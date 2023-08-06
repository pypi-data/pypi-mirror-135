import numpy as np
from .utils import (filter_code, get_copied_slices, get_document_fingerprints, find_fingerprint_overlap)

class CodeFingerprint:
    def __init__(self, code, name, k, win_size, boilerplate=[], language=None):
        filtered_code, offsets = filter_code(code, name, language)
        hashes, idx = get_document_fingerprints(filtered_code, k, win_size, boilerplate)
        
        self.raw_code = code
        self.filtered_code = filtered_code
        self.offsets = offsets
        self.hashes = hashes
        self.hash_idx = idx
        self.k = k

def compare_files(file1_data, file2_data):
   
    if file1_data.k != file2_data.k:
        raise ValueError("Code fingerprints must use the same noise threshold")
 
    idx1, idx2 = find_fingerprint_overlap(
        file1_data.hashes, file2_data.hashes,
        file1_data.hash_idx, file2_data.hash_idx)
    slices1 = get_copied_slices(idx1, file1_data.k)
   
    if len(slices1[0]) == 0:
        return 0

    token_overlap = np.sum(slices1[1] - slices1[0])

    if len(file1_data.filtered_code) > 0:
        similarity = token_overlap / len(file1_data.filtered_code)
    else:
        similarity = 0

    return similarity

class CopyDetector:

    def __init__(self, code1="", code2="", extension="python",
                 noise_t=25, guarantee_t=30, display_t=0.33):
   
        self.code1 = code1
        self.code2 = code2
        self.extension = extension
        self.noise_t = noise_t
        self.guarantee_t = guarantee_t
        self.display_t = display_t
        self.window_size = self.guarantee_t - self.noise_t + 1
     

    def run(self):
        self.file_data = self._preprocess_code()
        
        self.similarity_matrix = np.full((2, 2), -1, dtype=np.float64)
        self.token_overlap_matrix = np.full((2, 2), -1)
        self.slice_matrix = [[np.array([]) for _ in range(2)] for _ in range(2)]
     
        similarity = compare_files(self.file_data["code1"], self.file_data["code2"])
        print( similarity )
     
    def _preprocess_code(self):
        boilerplate_hashes = np.unique(np.array([]))
       
        file_data = {}
        try:
            file_data["code1"] = CodeFingerprint(
                self.code1, "code1", self.noise_t, self.window_size,
                boilerplate_hashes, self.extension)
            
            file_data["code2"] = CodeFingerprint(
                self.code2, "code2", self.noise_t, self.window_size,
                boilerplate_hashes, self.extension)
            
        except UnicodeDecodeError:
            print("Skipping: Code is not ASCII text")
          
        return file_data
