"""Train the contamination CNN model from multimodal sensor and image data."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import pandas as pd
import torch
from torch import nn

from ..contamination_cnn import ContaminationCNN, create_dataloader, set_deterministic_seed
from ..model_registry import ModelRegistry

LOGGER = logging.getLogger(__name__)


def train_contamination_model(
    input_csv: str | Path,
    image_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 1e-3,
    metadata_columns: list[str] | None = None,
    gas_columns: list[str] | None = None,
    seed: int | None = None,
) -> dict[str, float | str]:
    """Train the contamination CNN and register the model artifact."""
    set_deterministic_seed(seed)

    df = pd.read_csv(input_csv)
    if df.empty:
        raise ValueError("Input CSV is empty.")

    output_root = Path(output_dir or os.getenv("MODEL_STORAGE_PATH", "/models")) / "contamination_cnn"
    output_root.mkdir(parents=True, exist_ok=True)

    default_metadata = [
        "temperature", "humidity", "fill_level", "sensor_1", "sensor_2", "sensor_3", "sensor_4", "sensor_5"
    ]
    default_gas = ["gas_1", "gas_2", "gas_3", "gas_4", "gas_5", "gas_6", "gas_7", "gas_8"]

    metadata_cols = metadata_columns or default_metadata
    gas_cols = gas_columns or default_gas

    train_loader = create_dataloader(
        dataframe=df,
        batch_size=batch_size,
        image_column="image_path",
        label_column="label",
        metadata_columns=metadata_cols,
        gas_columns=gas_cols,
        image_root=Path(image_dir) if image_dir is not None else None,
    )

    sensor_dim = len(metadata_cols)
    gas_dim = len(gas_cols)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ContaminationCNN(sensor_dim=sensor_dim, gas_dim=gas_dim, metadata_dim=sensor_dim, num_classes=2).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    running_loss = 0.0
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()

            image = batch.get("image").to(device) if "image" in batch else None
            sensor = batch.get("sensor").to(device) if "sensor" in batch else None
            gas_signal = batch.get("gas_signal").to(device) if "gas_signal" in batch else None
            metadata = sensor.clone() if sensor is not None else None
            logits = model(image=image, sensor=sensor, gas_signal=gas_signal, metadata=metadata)
            labels = batch["labels"].to(device)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / max(1, len(train_loader))
        running_loss = avg_loss
        LOGGER.info("Epoch %s/%s - loss: %.4f", epoch + 1, epochs, avg_loss)

    model_path = output_root / f"contamination_cnn_{epochs}.pt"
    torch.save(model, model_path)

    registry = ModelRegistry()
    registry.register_model(
        model_name="contamination_cnn",
        model_type="torch",
        artifact_path=model_path,
        metrics={"epochs": epochs, "training_loss": float(running_loss)},
    )

    return {"training_loss": float(running_loss), "model_path": str(model_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the contamination CNN model.")
    parser.add_argument("--input-csv", type=str, required=True, help="Path to training CSV.")
    parser.add_argument("--image-dir", type=str, default=None, help="Directory containing images.")
    parser.add_argument("--output-dir", type=str, default=None, help="Where to save the model.")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Learning rate.")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    metrics = train_contamination_model(
        input_csv=args.input_csv,
        image_dir=args.image_dir,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        seed=args.seed,
    )
    LOGGER.info("Training complete: %s", metrics)


if __name__ == "__main__":
    main()
