import random
import hashlib

class Codec:
    def __init__(self):
        self.delimiter = '#'
        self.checksum_delimiter = '|'
    
    def encode(self, strs):
        if not strs:
            return "0|" + self._calculate_checksum("")
        
        encoded_parts = []
        for s in strs:
            encoded_parts.append(f"{len(s)}{self.delimiter}{s}")
        
        encoded_data = ''.join(encoded_parts)
        checksum = self._calculate_checksum(encoded_data)
        
        return encoded_data + self.checksum_delimiter + checksum
    
    def decode(self, s):
        if not s:
            return False, []
        
        if self.checksum_delimiter not in s:
            return False, []
        
        parts = s.rsplit(self.checksum_delimiter, 1)
        if len(parts) != 2:
            return False, []
        
        encoded_data, received_checksum = parts
        expected_checksum = self._calculate_checksum(encoded_data)
        
        if received_checksum != expected_checksum:
            partial = self._extract_partial_data(encoded_data)
            return False, partial
        
        if not encoded_data:
            return True, []
        
        decoded_strings = []
        i = 0
        
        while i < len(encoded_data):
            delimiter_pos = encoded_data.find(self.delimiter, i)
            if delimiter_pos == -1:
                return False, decoded_strings
            
            try:
                length_str = encoded_data[i:delimiter_pos]
                length = int(length_str)
            except ValueError:
                return False, decoded_strings
            
            start_pos = delimiter_pos + 1
            end_pos = start_pos + length
            
            if end_pos > len(encoded_data):
                return False, decoded_strings
            
            string_data = encoded_data[start_pos:end_pos]
            decoded_strings.append(string_data)
            
            i = end_pos
        
        return True, decoded_strings
    
    def transmit(self, strs):
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            encoded = self.encode(strs)
            transmitted = self._noisy_channel(encoded)
            is_valid, result = self.decode(transmitted)
            
            if is_valid:
                return result
            
            print(f"Attempt {attempt}: Transmission tampered. Partial decoded: {result}")
            print("Requesting resend...")
        
        raise RuntimeError("Failed to transmit after maximum attempts")
    
    def _calculate_checksum(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()[:8]
    
    def _extract_partial_data(self, encoded_data):
        decoded_strings = []
        i = 0
        
        while i < len(encoded_data):
            try:
                delimiter_pos = encoded_data.find(self.delimiter, i)
                if delimiter_pos == -1:
                    break
                
                length_str = encoded_data[i:delimiter_pos]
                if not length_str.isdigit():
                    i = delimiter_pos + 1
                    continue
                
                length = int(length_str)
                start_pos = delimiter_pos + 1
                end_pos = start_pos + length
                
                if end_pos > len(encoded_data):
                    break
                
                string_data = encoded_data[start_pos:end_pos]
                decoded_strings.append(string_data)
                i = end_pos
                
            except (ValueError, IndexError):
                i += 1
        
        return decoded_strings
    
    def _noisy_channel(self, data):
        if random.random() < 0.7:
            return data
        
        data_list = list(data)
        corruption_types = ['replace_char', 'change_length', 'remove_char']
        corruption_type = random.choice(corruption_types)
        
        if corruption_type == 'replace_char' and len(data_list) > 0:
            pos = random.randint(0, len(data_list) - 1)
            data_list[pos] = random.choice('abcdefghijklmnopqrstuvwxyz@$%^&*')
        
        elif corruption_type == 'change_length' and self.delimiter in data:
            for i in range(len(data_list)):
                if data_list[i].isdigit() and i + 1 < len(data_list) and data_list[i + 1] == self.delimiter:
                    data_list[i] = str(random.randint(1, 9))
                    break
        
        elif corruption_type == 'remove_char' and len(data_list) > 1:
            pos = random.randint(0, len(data_list) - 1)
            data_list.pop(pos)
        
        return ''.join(data_list)

def test_codec():
    codec = Codec()
    
    print("=== Test Case 1 ===")
    strs1 = ["leet", "code", "love", "you"]
    print(f"Input: {strs1}")
    
    encoded = codec.encode(strs1)
    print(f"Encoded: {encoded}")
    
    is_valid, decoded = codec.decode(encoded)
    print(f"Clean decode - Valid: {is_valid}, Result: {decoded}")
    
    print("Testing transmission with potential tampering...")
    result = codec.transmit(strs1)
    print(f"Final transmitted result: {result}")
    print()
    
    print("=== Test Case 2 ===")
    strs2 = ["we", "say", ":", "yes"]
    print(f"Input: {strs2}")
    
    encoded2 = codec.encode(strs2)
    print(f"Encoded: {encoded2}")
    
    result2 = codec.transmit(strs2)
    print(f"Final transmitted result: {result2}")
    print()
    
    print("=== Test Case 3 (Empty) ===")
    strs3 = []
    print(f"Input: {strs3}")
    result3 = codec.transmit(strs3)
    print(f"Final transmitted result: {result3}")
    print()
    
    print("=== Test Case 4 (Single string) ===")
    strs4 = ["hello"]
    print(f"Input: {strs4}")
    result4 = codec.transmit(strs4)
    print(f"Final transmitted result: {result4}")

if __name__ == "__main__":
    random.seed(42)
    test_codec()