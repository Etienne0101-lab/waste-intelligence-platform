"""Contamination CNN module for multimodal contamination detection.

This module supports contamination classification using:
- sensor metadata
- optional image data
- optional audio/gas sensor signals
"""

from __future__ import annotations

import logging
import os
import random
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

LOGGER = logging.getLogger(__name__)


def set_deterministic_seed(seed: int | None = None) -> int:
    """Set deterministic random seed across Python, NumPy, and PyTorch."""
    resolved_seed = int(seed or int(os.getenv("MODEL_SEED", "42")))
    random.seed(resolved_seed)
    np.random.seed(resolved_seed)
    torch.manual_seed(resolved_seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(resolved_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    return resolved_seed


class ContaminationDataset(Dataset):
    """Dataset wrapper for contamination classification samples."""

    def __init__(
        self,
        dataframe: pd.DataFrame,
        image_column: str = "image_path",
        label_column: str = "label",
        metadata_columns: Sequence[str] | None = None,
        gas_columns: Sequence[str] | None = None,
        transform: Any | None = None,
        image_root: str | Path | None = None,
    ) -> None:
        if dataframe.empty:
            raise ValueError("Input dataframe is empty.")
        self.dataframe = dataframe.reset_index(drop=True)
        self.image_column = image_column
        self.label_column = label_column
        self.metadata_columns = list(metadata_columns or [])
        self.gas_columns = list(gas_columns or [])
        self.transform = transform
        self.image_root = Path(image_root) if image_root else None

    def __len__(self) -> int:
        return len(self.dataframe)

    def __getitem__(self, index: int) -> dict[str, Any]:
        row = self.dataframe.iloc[index]

        image_tensor = None
        if self.image_column in row.index and pd.notna(row[self.image_column]):
            image_path = row[self.image_column]
            if self.image_root is not None and not Path(image_path).is_absolute():
                image_path = str(self.image_root / image_path)
            image_tensor = self._load_image(image_path)

        sensor_features: list[float] = []
        for column in self.metadata_columns:
            if column in row.index and pd.notna(row[column]):
                sensor_features.append(float(row[column]))

        gas_signal: list[float] = []
        for column in self.gas_columns:
            if column in row.index and pd.notna(row[column]):
                gas_signal.append(float(row[column]))

        label = int(row[self.label_column])
        return {
            "image": image_tensor,
            "sensor": torch.tensor(sensor_features, dtype=torch.float32) if sensor_features else None,
            "gas_signal": torch.tensor(gas_signal, dtype=torch.float32) if gas_signal else None,
            "label": torch.tensor(label, dtype=torch.long),
        }

    @staticmethod
    def _load_image(image_path: str) -> torch.Tensor:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow is required for image handling in contamination CNN training.") from exc

        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img_array = np.asarray(img, dtype=np.float32) / 255.0
            tensor = torch.from_numpy(np.transpose(img_array, (2, 0, 1)))
            return tensor

    @staticmethod
    def _normalize_features(values: Sequence[float]) -> list[float]:
        return [float(value) for value in values]


class ContaminationCNN(nn.Module):
    """Multimodal contamination model handling image, sensor, gas, and metadata inputs."""

    def __init__(
        self,
        image_channels: int = 3,
        sensor_dim: int = 8,
        gas_dim: int = 8,
        metadata_dim: int = 8,
        num_classes: int = 2,
    ) -> None:
        super().__init__()
        self.image_channels = image_channels
        self.sensor_dim = sensor_dim
        self.gas_dim = gas_dim
        self.metadata_dim = metadata_dim

        self.image_encoder = nn.Sequential(
            nn.Conv2d(image_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )

        image_out_dim = 128
        sensor_out_dim = 32
        gas_out_dim = 32
        metadata_out_dim = 32

        self.sensor_mlp = nn.Sequential(
            nn.Linear(sensor_dim, sensor_out_dim),
            nn.ReLU(),
            nn.Linear(sensor_out_dim, sensor_out_dim),
        )
        self.gas_mlp = nn.Sequential(
            nn.Linear(gas_dim, gas_out_dim),
            nn.ReLU(),
            nn.Linear(gas_out_dim, gas_out_dim),
        )
        self.metadata_mlp = nn.Sequential(
            nn.Linear(metadata_dim, metadata_out_dim),
            nn.ReLU(),
            nn.Linear(metadata_out_dim, metadata_out_dim),
        )

        self.classifier = nn.Sequential(
            nn.Linear(image_out_dim + sensor_out_dim + gas_out_dim + metadata_out_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes),
        )

    def forward(
        self,
        image: torch.Tensor | None = None,
        sensor: torch.Tensor | None = None,
        gas_signal: torch.Tensor | None = None,
        metadata: torch.Tensor | None = None,
    ) -> torch.Tensor:
        features: list[torch.Tensor] = []

        if image is not None:
            if image.dim() == 3:
                image = image.unsqueeze(0)
            if image.shape[1] != self.image_channels:
                raise ValueError(
                    f"Expected image channels={self.image_channels}, got {image.shape[1]}."
                )
            image_features = self.image_encoder(image)
            image_features = image_features.view(image_features.size(0), -1)
            features.append(image_features)

        if sensor is not None:
            if sensor.dim() == 1:
                sensor = sensor.unsqueeze(0)
            if sensor.shape[-1] != self.sensor_dim:
                raise ValueError(f"Expected sensor_dim={self.sensor_dim}, got {sensor.shape[-1]}.")
            features.append(self.sensor_mlp(sensor))

        if gas_signal is not None:
            if gas_signal.dim() == 1:
                gas_signal = gas_signal.unsqueeze(0)
            if gas_signal.shape[-1] != self.gas_dim:
                raise ValueError(f"Expected gas_dim={self.gas_dim}, got {gas_signal.shape[-1]}.")
            features.append(self.gas_mlp(gas_signal))

        if metadata is not None:
            if metadata.dim() == 1:
                metadata = metadata.unsqueeze(0)
            if metadata.shape[-1] != self.metadata_dim:
                raise ValueError(f"Expected metadata_dim={self.metadata_dim}, got {metadata.shape[-1]}.")
            features.append(self.metadata_mlp(metadata))

        if not features:
            raise ValueError("At least one of image, sensor, gas_signal, or metadata must be provided.")

        merged = torch.cat(features, dim=1)
        return self.classifier(merged)


def collate_batch(batch: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Collate a list of samples into a single batch dictionary."""
    images = [item["image"] for item in batch if item["image"] is not None]
    sensors = [item["sensor"] for item in batch if item["sensor"] is not None]
    gas_signals = [item["gas_signal"] for item in batch if item["gas_signal"] is not None]
    labels = torch.stack([item["label"] for item in batch])

    batch_dict: dict[str, Any] = {"labels": labels}
    if images:
        batch_dict["image"] = torch.stack(images)
    if sensors:
        batch_dict["sensor"] = torch.stack(sensors)
    if gas_signals:
        batch_dict["gas_signal"] = torch.stack(gas_signals)
    return batch_dict


def prepare_training_dataframe(
    dataframe: pd.DataFrame,
    label_column: str = "label",
    image_column: str = "image_path",
    metadata_columns: Sequence[str] | None = None,
    gas_columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Validate and prepare a contamination training dataframe."""
    required_columns = [label_column]
    if image_column is not None:
        required_columns.append(image_column)
    if metadata_columns:
        required_columns.extend(metadata_columns)
    if gas_columns:
        required_columns.extend(gas_columns)

    missing = [column for column in required_columns if column not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = dataframe.copy()
    if label_column in df.columns:
        df[label_column] = df[label_column].astype(int)
    return df


def create_dataloader(
    dataframe: pd.DataFrame,
    batch_size: int = 32,
    image_column: str = "image_path",
    label_column: str = "label",
    metadata_columns: Sequence[str] | None = None,
    gas_columns: Sequence[str] | None = None,
    image_root: str | Path | None = None,
) -> DataLoader:
    """Create a DataLoader for contamination training."""
    dataset = ContaminationDataset(
        dataframe=prepare_training_dataframe(
            dataframe,
            label_column=label_column,
            image_column=image_column,
            metadata_columns=metadata_columns,
            gas_columns=gas_columns,
        ),
        image_column=image_column,
        label_column=label_column,
        metadata_columns=metadata_columns,
        gas_columns=gas_columns,
        image_root=image_root,
    )
    return DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_batch)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Contamination CNN module loaded successfully.")
