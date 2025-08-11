import os
import numpy as np
from collections import defaultdict

class HypercubeLoader:
    def __init__(self, root_path, height=512, width=640):
        """
        Initialize the HypercubeLoader to load frames from i_j folders.
        
        Parameters:
            root_path (str): Path to the root directory containing i_j folders
            height (int): Height of each frame (default: 512)
            width (int): Width of each frame (default: 640)
        """
        self.root_path = root_path
        self.height = height
        self.width = width
        self.folder_groups = defaultdict(list)
        self._scan_folders()
    
    def _scan_folders(self):
        """Scan root directory and categorize folders into groups."""
        for name in os.listdir(self.root_path):
            if not os.path.isdir(os.path.join(self.root_path, name)):
                continue
            parts = name.split('_')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                i, j = int(parts[0]), int(parts[1])
                self.folder_groups[(i, j)] = name
        
    def _get_ordered_folders(self):
        """
        Order folders in the required sequence:
        1. All i_0 where i ≥ 1 (sorted by i)
        2. All 0_j where j ≥ 1 (sorted by j)
        3. All remaining i_j combinations (sorted lexicographically)
        """
        # Separate special cases
        i0_folders = []
        zero_j_folders = []
        other_folders = []
        
        for (i, j), name in self.folder_groups.items():
            if i == 0 and j == 0:
                continue  # Will handle separately
            elif j == 0 and i >= 1:
                i0_folders.append((i, name))
            elif i == 0 and j >= 1:
                zero_j_folders.append((j, name))
            else:
                other_folders.append(((i, j), name))
        
        # Sort each group
        i0_folders_sorted = [name for _, name in sorted(i0_folders)]
        zero_j_folders_sorted = [name for _, name in sorted(zero_j_folders)]
        other_folders_sorted = [name for _, name in sorted(other_folders)]
        
        return i0_folders_sorted + zero_j_folders_sorted + other_folders_sorted
    
    def _load_bin(self, file_path, dtype):
        """Load and reshape a binary frame file."""
        data = np.fromfile(file_path, dtype=dtype)
        return data.reshape((self.height, self.width))
    
    def load_frames(self, frame_type, frame_index):
        """
        Load frames organized in the specified order along with full transmission frame.
        
        Parameters:
            frame_type (str): 'calibrated', 'raw', or 'temperature'
            frame_index (int): Index of the frame to load
            
        Returns:
            hypercube (np.ndarray): Stacked frames in specified order (3D array)
            full_transmission (np.ndarray): Frame from 0_0 folder (2D array)
        """
        if frame_type not in ['calibrated', 'raw', 'temperature']:
            raise ValueError("Invalid frame type. Choose 'calibrated', 'raw', or 'temperature'")
        
        # Determine dtype based on frame type
        dtype = np.float32 if frame_type == 'temperature' else np.uint16
        
        # Get ordered folders (excluding 0_0)
        ordered_folders = self._get_ordered_folders()
        frames = []
        
        # Load full transmission frame (0_0) if exists
        full_transmission = None
        if (0, 0) in self.folder_groups:
            folder_name = self.folder_groups[(0, 0)]
            file_path = os.path.join(self.root_path, folder_name, f"{frame_type}_{frame_index}.bin")
            if os.path.exists(file_path):
                full_transmission = self._load_bin(file_path, dtype)
        
        # Load frames from all other folders in specified order
        for folder in ordered_folders:
            file_path = os.path.join(self.root_path, folder, f"{frame_type}_{frame_index}.bin")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Frame not found: {file_path}")
            frame = self._load_bin(file_path, dtype)
            frames.append(frame)
        
        # Stack all frames to create hypercube
        hypercube = np.stack(frames) if frames else np.array([])
        
        return hypercube, full_transmission