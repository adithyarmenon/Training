import random
import hashlib

class Codec:
    def __init__(self):
        self.delimiter = '#'
        self.checksum_delimiter = '|'
    
    def encode(self, strs):
        """
        Encodes a list of strings with length prefixes and checksum for integrity.
        Format: length1#string1length2#string2...lengthN#stringN|checksum
        """
        if not strs:
            return "0|" + self._calculate_checksum("")
        
        encoded_parts = []
        for s in strs:
            encoded_parts.append(f"{len(s)}{self.delimiter}{s}")
        
        encoded_data = ''.join(encoded_parts)
        checksum = self._calculate_checksum(encoded_data)
        
        return encoded_data + self.checksum_delimiter + checksum
    
    def decode(self, s):
        """
        Decodes string with tamper detection.
        Returns (is_valid, decoded_strings or partial_decoded)
        """
        if not s:
            return False, []
        
        # Check for checksum
        if self.checksum_delimiter not in s:
            return False, []
        
        parts = s.rsplit(self.checksum_delimiter, 1)
        if len(parts) != 2:
            return False, []
        
        encoded_data, received_checksum = parts
        expected_checksum = self._calculate_checksum(encoded_data)
        
        # If checksums don't match, data is tampered
        if received_checksum != expected_checksum:
            # Try to extract partial data
            partial = self._extract_partial_data(encoded_data)
            return False, partial
        
        # Checksums match, proceed with normal decoding
        if not encoded_data:
            return True, []
        
        decoded_strings = []
        i = 0
        
        while i < len(encoded_data):
            # Find the delimiter
            delimiter_pos = encoded_data.find(self.delimiter, i)
            if delimiter_pos == -1:
                # No more delimiters, data might be corrupted
                return False, decoded_strings
            
            # Extract length
            try:
                length_str = encoded_data[i:delimiter_pos]
                length = int(length_str)
            except ValueError:
                # Invalid length format
                return False, decoded_strings
            
            # Check bounds
            start_pos = delimiter_pos + 1
            end_pos = start_pos + length
            
            if end_pos > len(encoded_data):
                # Not enough data for this string
                return False, decoded_strings
            
            # Extract the string
            string_data = encoded_data[start_pos:end_pos]
            decoded_strings.append(string_data)
            
            i = end_pos
        
        return True, decoded_strings
    
    def transmit(self, strs):
        """
        Simulates transmission with potential tampering and automatic retry.
        """
        max_attempts = 10  # Prevent infinite loops
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            # Encode the data
            encoded = self.encode(strs)
            
            # Simulate transmission through noisy channel
            transmitted = self._noisy_channel(encoded)
            
            # Try to decode
            is_valid, result = self.decode(transmitted)
            
            if is_valid:
                return result
            
            # If tampered, we have partial data
            print(f"Attempt {attempt}: Transmission tampered. Partial decoded: {result}")
            print("Requesting resend...")
        
        # If we get here, something is seriously wrong
        raise RuntimeError("Failed to transmit after maximum attempts")
    
    def _calculate_checksum(self, data):
        """Calculate MD5 checksum for integrity checking."""
        return hashlib.md5(data.encode('utf-8')).hexdigest()[:8]  # Use first 8 chars for efficiency
    
    def _extract_partial_data(self, encoded_data):
        """
        Extract as much valid data as possible from corrupted transmission.
        """
        decoded_strings = []
        i = 0
        
        while i < len(encoded_data):
            try:
                # Find the delimiter
                delimiter_pos = encoded_data.find(self.delimiter, i)
                if delimiter_pos == -1:
                    break
                
                # Extract and validate length
                length_str = encoded_data[i:delimiter_pos]
                if not length_str.isdigit():
                    # Skip invalid length, try to find next valid pattern
                    i = delimiter_pos + 1
                    continue
                
                length = int(length_str)
                start_pos = delimiter_pos + 1
                end_pos = start_pos + length
                
                # Check if we have enough data
                if end_pos > len(encoded_data):
                    break
                
                # Extract the string
                string_data = encoded_data[start_pos:end_pos]
                decoded_strings.append(string_data)
                i = end_pos
                
            except (ValueError, IndexError):
                # Skip corrupted part and try next character
                i += 1
        
        return decoded_strings
    
    def _noisy_channel(self, data):
        """
        Simulates a noisy transmission channel that may corrupt data.
        """
        # Randomly decide if transmission is corrupted (30% chance)
        if random.random() < 0.7:  # 70% chance of clean transmission
            return data
        
        # Corrupt the data
        data_list = list(data)
        corruption_types = ['replace_char', 'change_length', 'remove_char']
        corruption_type = random.choice(corruption_types)
        
        if corruption_type == 'replace_char' and len(data_list) > 0:
            # Replace a random character
            pos = random.randint(0, len(data_list) - 1)
            data_list[pos] = random.choice('abcdefghijklmnopqrstuvwxyz@$%^&*')
        
        elif corruption_type == 'change_length' and self.delimiter in data:
            # Change a length number
            for i in range(len(data_list)):
                if data_list[i].isdigit() and i + 1 < len(data_list) and data_list[i + 1] == self.delimiter:
                    data_list[i] = str(random.randint(1, 9))
                    break
        
        elif corruption_type == 'remove_char' and len(data_list) > 1:
            # Remove a random character
            pos = random.randint(0, len(data_list) - 1)
            data_list.pop(pos)
        
        return ''.join(data_list)


# Test the implementation
def test_codec():
    codec = Codec()
    
    print("=== Test Case 1 ===")
    strs1 = ["leet", "code", "love", "you"]
    print(f"Input: {strs1}")
    
    # Test encoding
    encoded = codec.encode(strs1)
    print(f"Encoded: {encoded}")
    
    # Test clean decoding
    is_valid, decoded = codec.decode(encoded)
    print(f"Clean decode - Valid: {is_valid}, Result: {decoded}")
    
    # Test transmission (may require multiple attempts)
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

# Run tests
if __name__ == "__main__":
    # Set random seed for reproducible testing
    random.seed(42)
    test_codec()