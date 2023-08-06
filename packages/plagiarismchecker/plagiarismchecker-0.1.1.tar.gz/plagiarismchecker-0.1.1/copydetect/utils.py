from pygments import lexers, token
import pygments.util
import numpy as np
import logging

try:
    from .winnow import _winnow
except (ModuleNotFoundError, ImportError):
    from .pywinnow import _winnow

def filter_code(code, filename, language=None):
    try:
        if language is not None:
            lexer = lexers.get_lexer_by_name(language)
        else:
            lexer = lexers.get_lexer_for_filename(filename)
        tokens = lexer.get_tokens(code)
    except pygments.util.ClassNotFound:
        logging.warning(f"{filename} not tokenized: unknown file extension")
        return code, np.array([])

    if lexer == pygments.lexers.TextLexer:
        logging.warning(f"did not tokenize plaintext file {filename}")
        return code, np.array([])

    out_code = ""
    offset = 0
    offsets = [[0,0]]
    variable_tokens = {token.Name, token.Name.Variable, token.Name.Attribute}
    for t in tokens:
        if t[0] in variable_tokens:
            out_code += "V"
            offsets.append([len(out_code) - 1, offset])
            offset += len(t[1]) - 1
        elif t[0] in token.Name.Function:
            out_code += "F"
            offsets.append([len(out_code) - 1, offset])
            offset += len(t[1]) - 1
        elif t[0] in token.Name.Class:
            out_code += "O"
            offsets.append([len(out_code) - 1, len(t[1]) - 1])
            offset += len(t[1]) - 1
        elif t[0] == token.Comment.Preproc or t[0] == token.Comment.Hashbang:
            out_code += "P"
            offsets.append([len(out_code) - 1, offset])
            offset += len(t[1]) - 1
        elif t[0] in token.Text or t[0] in token.Comment:
            offsets.append([len(out_code) - 1, offset])
            offset += len(t[1])
        elif t[0] in token.Literal.String:
            if t[1] == "'" or t[1] == '"':
                out_code += '"'
            else:
                out_code += "S"
                offsets.append([len(out_code) - 1, offset])
                offset += len(t[1]) - 1
        else:
            out_code += t[1]
    return out_code, np.array(offsets)

def hashed_kgrams(string, k):
    hashes = [hash(string[offset:offset+k])
              for offset in range(len(string) - k + 1)]
    return np.array(hashes)

def winnow(hashes, window_size, remove_duplicates=True):
    if window_size < 1:
        raise ValueError("window_size must be greater than 0")

    if window_size == 1:
        selected_hashes = hashes
        selected_idx = np.arange(len(hashes))
    else:
        selected_idx = _winnow(hashes, window_size)
        selected_hashes = hashes[selected_idx]

    if remove_duplicates:
        selected_hashes, unique_idx = np.unique(selected_hashes,
                                                return_index=True)
        selected_idx = selected_idx[unique_idx]

    return selected_hashes, selected_idx

def get_copied_slices(idx, k):

    if len(idx) == 0:
        return np.array([[],[]])

    # determine the gaps between slices (called skips)
    sorted_idx = np.sort(idx)
    next_idx = np.concatenate([sorted_idx[1:], [0]])
    skips = np.where(next_idx - sorted_idx > k - 1)[0]

    # use the elements around the gaps to compute slice start/ends
    slice_starts = np.concatenate([[sorted_idx[0]], sorted_idx[skips + 1]])
    slice_ends = np.concatenate([sorted_idx[skips]+k, [sorted_idx[-1]+k]])

    return np.array([slice_starts, slice_ends])

def get_document_fingerprints(doc, k, window_size, boilerplate=[]):
    hashes, idx = winnow(hashed_kgrams(doc, k=k), window_size=window_size)
    if len(boilerplate) > 0:
        _, overlap_idx, _ = np.intersect1d(hashes, boilerplate,
                                           return_indices=True,
                                           assume_unique=True)
        idx = np.delete(idx, overlap_idx)
        hashes = np.delete(hashes, overlap_idx)
    return hashes, idx

def find_fingerprint_overlap(hashes1, hashes2, idx1, idx2):
    overlap, ol_idx1, ol_idx2 = np.intersect1d(hashes1, hashes2,
        return_indices=True, assume_unique=True)

    return idx1[ol_idx1], idx2[ol_idx2]
