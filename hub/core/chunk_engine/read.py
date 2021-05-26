import os
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from .chunker import join_chunks

from hub import constants
from hub.util.keys import get_meta_key, get_index_map_key

from hub.core.typing import StorageProvider
from typing import Callable, List, Union


def read_tensor_meta(key: str, storage: StorageProvider):
    return pickle.loads(storage[get_meta_key(key)])


def read_dataset_meta(storage: StorageProvider):
    return pickle.loads(storage[constants.META_FILENAME])


def read_array(
    key: str,
    storage: StorageProvider,
    array_slice: slice = slice(None),
) -> np.ndarray:
    """Read and join chunks into an array from storage.

    Args:
        key (str): Key for where the chunks, index_map, and meta are located in `storage` relative to it's root.
        array_slice (slice): Slice that represents which samples to read. Default = slice representing all samples.
        storage (StorageProvider): StorageProvider for reading the chunks, index_map, and meta.

    Returns:
        np.ndarray: Array containing the sample(s) in the `array_slice` slice.
    """

    # TODO: don't use pickle
    meta = read_tensor_meta(key, storage)
    index_map = pickle.loads(storage[get_index_map_key(key)])

    def read_samples(index_entry):
        chunks = []
        for chunk_name in index_entry["chunk_names"]:
            chunk_key = os.path.join(key, "chunks", chunk_name)
            chunk = storage[chunk_key]

            chunks.append(chunk)

        combined_bytes = join_chunks(
            chunks,
            index_entry["start_byte"],
            index_entry["end_byte"],
        )

        out_array = np.frombuffer(combined_bytes, dtype=meta["dtype"])
        return out_array.reshape(index_entry["shape"])

    with ThreadPoolExecutor() as pool:
        samples = list(pool.map(read_samples, index_map[array_slice]))
    return np.array(samples)