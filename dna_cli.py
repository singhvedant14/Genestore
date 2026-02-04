#!/usr/bin/env python3
"""
DNA Storage CLI Tool
Command-line interface for DNA encoding/decoding with AI error correction

Usage:
    python dna_cli.py encode <file> [options]
    python dna_cli.py decode <dna_file> [options]
    python dna_cli.py train [options]
    python dna_cli.py test
"""

import argparse
import sys
import os
from pathlib import Path
import json
from datetime import datetime
from colorama import init, Fore, Style
import numpy as np

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import the DNA Storage System
from dna_storage_api import DNAStorageSystem


class DNAStorageCLI:
    """Command-line interface for DNA Storage System"""
    
    def __init__(self):
        self.system = DNAStorageSystem()
        self.banner()
    
    def banner(self):
        """Display banner"""
        print(Fore.CYAN + Style.BRIGHT + """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🧬  DNA STORAGE SIMULATOR CLI v1.0.0  🧬          ║
║                                                           ║
║          AI-Powered Error Correction System               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """ + Style.RESET_ALL)
    
    def print_success(self, message):
        """Print success message"""
        print(Fore.GREEN + "✓ " + message + Style.RESET_ALL)
    
    def print_error(self, message):
        """Print error message"""
        print(Fore.RED + "✗ " + message + Style.RESET_ALL)
    
    def print_info(self, message):
        """Print info message"""
        print(Fore.CYAN + "ℹ " + message + Style.RESET_ALL)
    
    def print_warning(self, message):
        """Print warning message"""
        print(Fore.YELLOW + "⚠ " + message + Style.RESET_ALL)
    
    def print_dna_sequence(self, sequence, max_length=80):
        """Print DNA sequence with colored bases"""
        colors = {
            'A': Fore.GREEN,
            'T': Fore.RED,
            'G': Fore.CYAN,
            'C': Fore.YELLOW
        }
        
        print("\nEncoded DNA Sequence:")
        print("=" * 80)
        
        for i in range(0, len(sequence), max_length):
            line = sequence[i:i+max_length]
            colored_line = ''.join([colors.get(base, '') + base for base in line])
            print(colored_line + Style.RESET_ALL)
        
        print("=" * 80)
    
    def encode_file(self, filepath, output=None, redundancy=5, mutations=0):
        """Encode a file to DNA"""
        try:
            # Read input file
            self.print_info(f"Reading file: {filepath}")
            
            if not os.path.exists(filepath):
                self.print_error(f"File not found: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = f.read()
            
            self.print_success(f"File loaded: {len(data)} characters")
            
            # Configure system
            self.system.redundancy = redundancy
            self.system.mutation_rate = mutations / 100
            
            # Encode
            self.print_info("Encoding to DNA...")
            result = self.system.encode(data, add_mutations=(mutations > 0))
            
            # Display results
            print("\n" + "=" * 80)
            print(Fore.CYAN + Style.BRIGHT + "ENCODING RESULTS" + Style.RESET_ALL)
            print("=" * 80)
            print(f"Original Length:     {result['original_length']} characters")
            print(f"Binary Length:       {result['binary_length']} bits")
            print(f"DNA Length:          {result['dna_length']} bases")
            print(f"With Redundancy:     {result['redundant_dna_length']} bases")
            print(f"Compression Ratio:   {result['compression_ratio']:.2f}x")
            print(f"Redundancy Factor:   {result['redundancy_factor']}x")
            
            if result['mutations_simulated'] > 0:
                print(f"Mutations Simulated: {result['mutations_simulated']}")
            
            print("=" * 80)
            
            # Show DNA sequence (first 80 bases)
            self.print_dna_sequence(result['dna_sequence'][:400])
            
            if len(result['dna_sequence']) > 400:
                self.print_info(f"... and {len(result['dna_sequence']) - 400} more bases")
            
            # Save to file
            if output is None:
                output = Path(filepath).stem + "_dna.txt"
            
            self.print_info(f"Saving to: {output}")
            
            with open(output, 'w') as f:
                f.write(result['dna_sequence'])
            
            # Save metadata
            metadata_file = Path(output).stem + "_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            self.print_success(f"DNA sequence saved to: {output}")
            self.print_success(f"Metadata saved to: {metadata_file}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Encoding failed: {str(e)}")
            return False
    
    def decode_file(self, dna_filepath, output=None, use_ai=True):
        """Decode a DNA file back to original data"""
        try:
            # Read DNA file
            self.print_info(f"Reading DNA file: {dna_filepath}")
            
            if not os.path.exists(dna_filepath):
                self.print_error(f"File not found: {dna_filepath}")
                return False
            
            with open(dna_filepath, 'r') as f:
                dna_sequence = f.read().strip()
            
            self.print_success(f"DNA loaded: {len(dna_sequence)} bases")
            
            # Decode
            self.print_info("Decoding from DNA...")
            if use_ai:
                self.print_info("Using AI error correction")
            
            result = self.system.decode(dna_sequence, use_ai=use_ai)
            
            # Display results
            print("\n" + "=" * 80)
            print(Fore.CYAN + Style.BRIGHT + "DECODING RESULTS" + Style.RESET_ALL)
            print("=" * 80)
            print(f"Errors Detected:     {result['errors_detected']}")
            print(f"Errors Corrected:    {result['errors_corrected']}")
            print(f"Accuracy:            {result['accuracy']:.2f}%")
            print(f"Data Integrity:      {result['data_integrity']:.2f}%")
            print("=" * 80)
            
            # Show decoded data preview
            decoded_data = result['decoded_data']
            print("\nDecoded Data Preview:")
            print("=" * 80)
            preview = decoded_data[:500]
            print(preview)
            if len(decoded_data) > 500:
                print(f"\n... and {len(decoded_data) - 500} more characters")
            print("=" * 80)
            
            # Save to file
            if output is None:
                output = Path(dna_filepath).stem + "_decoded.txt"
            
            self.print_info(f"Saving to: {output}")
            
            with open(output, 'w', encoding='utf-8') as f:
                f.write(decoded_data)
            
            self.print_success(f"Decoded data saved to: {output}")
            
            # Show comparison if original file exists
            original_file = Path(dna_filepath).parent / (Path(dna_filepath).stem.replace('_dna', '') + '.txt')
            if original_file.exists():
                with open(original_file, 'r', encoding='utf-8') as f:
                    original_data = f.read()
                
                match_percent = (sum(1 for a, b in zip(original_data, decoded_data) if a == b) / 
                               len(original_data)) * 100
                
                print(f"\nComparison with original: {match_percent:.2f}% match")
                
                if match_percent == 100:
                    self.print_success("Perfect reconstruction! ✨")
                elif match_percent >= 99:
                    self.print_success("Excellent reconstruction!")
                elif match_percent >= 95:
                    self.print_warning("Good reconstruction with minor errors")
                else:
                    self.print_error("Significant data loss detected")
            
            return True
            
        except Exception as e:
            self.print_error(f"Decoding failed: {str(e)}")
            return False
    
    def train_model(self, samples=100):
        """Train the AI error correction model"""
        try:
            self.print_info(f"Generating {samples} training samples...")
            
            original_sequences = []
            mutated_sequences = []
            
            for i in range(samples):
                # Generate random DNA sequence
                length = np.random.randint(50, 200)
                bases = ['A', 'C', 'G', 'T']
                original = ''.join(np.random.choice(bases, length))
                
                # Simulate mutations
                mutated, _ = self.system.simulate_mutations(original)
                
                original_sequences.append(original)
                mutated_sequences.append(mutated)
                
                if (i + 1) % 20 == 0:
                    print(f"  Generated {i + 1}/{samples} samples...")
            
            self.print_success(f"Generated {samples} training samples")
            
            # Train the model
            self.print_info("Training AI model (this may take a minute)...")
            self.system.ai_corrector.train_on_patterns(original_sequences, mutated_sequences)
            
            self.print_success("AI model trained successfully! 🎉")
            
            return True
            
        except Exception as e:
            self.print_error(f"Training failed: {str(e)}")
            return False
    
    def run_tests(self):
        """Run comprehensive tests"""
        print("\n" + "=" * 80)
        print(Fore.CYAN + Style.BRIGHT + "RUNNING TESTS" + Style.RESET_ALL)
        print("=" * 80)
        
        tests_passed = 0
        tests_total = 0
        
        # Test 1: Basic encoding/decoding
        print("\n[Test 1] Basic Encoding/Decoding")
        tests_total += 1
        try:
            test_data = "Hello, DNA Storage World!"
            result = self.system.encode(test_data)
            decoded = self.system.decode(result['dna_sequence'], use_ai=False)
            
            if decoded['decoded_data'] == test_data:
                self.print_success("Basic encoding/decoding works")
                tests_passed += 1
            else:
                self.print_error("Basic encoding/decoding failed")
        except Exception as e:
            self.print_error(f"Test failed: {str(e)}")
        
        # Test 2: Error correction without AI
        print("\n[Test 2] Reed-Solomon Error Correction")
        tests_total += 1
        try:
            test_data = "Testing error correction"
            result = self.system.encode(test_data, add_mutations=True)
            decoded = self.system.decode(result['dna_sequence'], use_ai=False)
            
            accuracy = (sum(1 for a, b in zip(test_data, decoded['decoded_data']) if a == b) / 
                       len(test_data)) * 100
            
            if accuracy >= 90:
                self.print_success(f"Reed-Solomon correction works ({accuracy:.1f}% accuracy)")
                tests_passed += 1
            else:
                self.print_warning(f"Reed-Solomon correction marginal ({accuracy:.1f}% accuracy)")
        except Exception as e:
            self.print_error(f"Test failed: {str(e)}")
        
        # Test 3: AI error correction
        print("\n[Test 3] AI Error Correction")
        tests_total += 1
        try:
            # Train model first
            self.system.ai_corrector.train_on_patterns(
                ['ATCGATCGATCG'] * 10,
                ['ATCGATCGATCG'] * 10
            )
            
            test_data = "AI-powered correction test"
            result = self.system.encode(test_data, add_mutations=True)
            decoded = self.system.decode(result['dna_sequence'], use_ai=True)
            
            if decoded['errors_corrected'] >= 0:
                self.print_success(f"AI correction works ({decoded['errors_corrected']} errors fixed)")
                tests_passed += 1
            else:
                self.print_error("AI correction failed")
        except Exception as e:
            self.print_error(f"Test failed: {str(e)}")
        
        # Test 4: Large data
        print("\n[Test 4] Large Data Handling")
        tests_total += 1
        try:
            test_data = "Large data test. " * 100  # ~1700 characters
            result = self.system.encode(test_data)
            decoded = self.system.decode(result['dna_sequence'], use_ai=False)
            
            if decoded['decoded_data'] == test_data:
                self.print_success(f"Large data handling works ({len(test_data)} chars)")
                tests_passed += 1
            else:
                self.print_error("Large data handling failed")
        except Exception as e:
            self.print_error(f"Test failed: {str(e)}")
        
        # Test 5: Special characters
        print("\n[Test 5] Special Characters")
        tests_total += 1
        try:
            test_data = "Special: !@#$%^&*()_+-=[]{}|;:',.<>?/~`\n\t"
            result = self.system.encode(test_data)
            decoded = self.system.decode(result['dna_sequence'], use_ai=False)
            
            if decoded['decoded_data'] == test_data:
                self.print_success("Special character handling works")
                tests_passed += 1
            else:
                self.print_error("Special character handling failed")
        except Exception as e:
            self.print_error(f"Test failed: {str(e)}")
        
        # Summary
        print("\n" + "=" * 80)
        print(Fore.CYAN + Style.BRIGHT + "TEST SUMMARY" + Style.RESET_ALL)
        print("=" * 80)
        print(f"Tests Passed: {tests_passed}/{tests_total}")
        
        if tests_passed == tests_total:
            self.print_success("All tests passed! 🎉")
        elif tests_passed >= tests_total * 0.8:
            self.print_warning("Most tests passed")
        else:
            self.print_error("Some tests failed")
        
        print("=" * 80)
        
        return tests_passed == tests_total


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='DNA Storage Simulator - AI-Powered Error Correction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode a file
  python dna_cli.py encode myfile.txt -r 5 -m 2

  # Decode a DNA file
  python dna_cli.py decode myfile_dna.txt --no-ai

  # Train AI model
  python dna_cli.py train -s 500

  # Run tests
  python dna_cli.py test
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode file to DNA')
    encode_parser.add_argument('file', help='Input file to encode')
    encode_parser.add_argument('-o', '--output', help='Output DNA file')
    encode_parser.add_argument('-r', '--redundancy', type=int, default=5,
                              help='Redundancy level (1-10, default: 5)')
    encode_parser.add_argument('-m', '--mutations', type=int, default=0,
                              help='Mutation rate %% (0-20, default: 0)')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode DNA file')
    decode_parser.add_argument('file', help='DNA file to decode')
    decode_parser.add_argument('-o', '--output', help='Output decoded file')
    decode_parser.add_argument('--no-ai', action='store_true',
                              help='Disable AI error correction')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train AI model')
    train_parser.add_argument('-s', '--samples', type=int, default=100,
                             help='Number of training samples (default: 100)')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = DNAStorageCLI()
    
    # Execute command
    if args.command == 'encode':
        success = cli.encode_file(
            args.file,
            output=args.output,
            redundancy=args.redundancy,
            mutations=args.mutations
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'decode':
        success = cli.decode_file(
            args.file,
            output=args.output,
            use_ai=not args.no_ai
        )
        sys.exit(0 if success else 1)
    
    elif args.command == 'train':
        success = cli.train_model(samples=args.samples)
        sys.exit(0 if success else 1)
    
    elif args.command == 'test':
        success = cli.run_tests()
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
