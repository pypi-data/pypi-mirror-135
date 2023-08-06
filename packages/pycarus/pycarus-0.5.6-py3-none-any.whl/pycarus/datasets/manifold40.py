import shutil
from pathlib import Path
from typing import Callable, List, Tuple, Union

import torch
from torch import Tensor
from torch.utils.data import Dataset

from pycarus.geometry.mesh import read_mesh
from pycarus.transforms.var import Compose
from pycarus.utils import download_and_extract


class Manifold40(Dataset):
    """Manifold40 Dataset, as proposed in
    Hu, Shi-Min, et al. "Subdivision-Based Mesh Convolution Networks."
    """

    def __init__(
        self,
        root: Union[Path, str],
        split: str,
        download: bool = False,
        vertices_transforms: List[Callable] = [],
        triangles_transforms: List[Callable] = [],
    ) -> None:
        """Create an instance of Manifold40 dataset.

        Args:
            root: The path to the root directory of the dataset.
            split: The split to use (only "train" or "test" allowed).
            download: Whether to download or not the dataset. If the root
                directory already exists, the dataset will not be downloaded
                in any case. Defaults to False.
            vertices_transforms: The transform to apply to the vertices of
                each item. Defaults to [].
            triangles_transforms: The transform to apply to the triangles of
                each item. Defaults to [].
        """
        if split not in ["train", "test"]:
            raise ValueError("Only train and test splits are available.")

        self.root = Path(root)
        if download:
            if self.root.exists():
                print("Dataset root already exists, not downloading.")
            else:
                print("Downloading dataset...")
                self.download()

        self.classes = sorted([s.name for s in self.root.iterdir()])

        self.paths: List[Path] = []
        self.labels: List[Tensor] = []

        for i, c in enumerate(self.classes):
            class_path = self.root / c / split

            items_paths = sorted(list(class_path.glob("*.obj")))
            for p in items_paths:
                self.paths.append(p)
                self.labels.append(torch.tensor(i, dtype=torch.long))

        self.vertices_transform = Compose(vertices_transforms)
        self.triangles_transform = Compose(triangles_transforms)

    def __len__(self) -> int:
        """Return the number of meshes in the dataset.

        Returns:
            The number of meshes in the dataset.
        """
        return len(self.paths)

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor, Tensor]:
        """Return the vertices, the triangles and the label at the given index.

        Args:
            index: The index of the required element.

        Returns:
            - A tensor with the vertices with shape (N, D). D can be 3, 6 or 9
                depending on the availability of normals and colors.
            - A tensor with the triangles with shape (M, D). D can be 3 or 6
                depending on the availability of normals.
            - A tensor with the label.
        """
        vertices, triangles = read_mesh(self.paths[index])
        vertices = self.vertices_transform(vertices)
        triangles = self.triangles_transform(triangles)
        return vertices, triangles, self.labels[index]

    def download(self) -> None:
        """Function to download the dataset."""
        url = "https://cloud.tsinghua.edu.cn/f/af5c682587cc4f9da9b8/?dl=1"
        path_temp = Path("/tmp")
        path_file_downloaded = path_temp / "manifold40.zip"
        download_and_extract(url, path_file_downloaded, path_temp)

        path_ds_extracted = path_temp / "Manifold40-MAPS-96-3"

        shutil.copytree(path_ds_extracted, self.root)
        shutil.rmtree(path_ds_extracted)

    def get_class(self, label: int) -> str:
        """Return the name of the class with the given label.

        Args:
            label: The numeric label of the required class.

        Returns:
            The name of the class corresponding to the given label.
        """
        return self.classes[label]
