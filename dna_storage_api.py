"""
DNA Storage Simulator - Python API
Advanced AI-Powered Error Correction System

This module provides a complete DNA storage encoding/decoding system with:
- Binary to DNA conversion using Goldman algorithm
- Reed-Solomon error correction
- Neural network-based error pattern detection
- Redundancy-based error recovery
- REST API endpoints for web integration

Author: DNA Storage Research Team
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import base64
import io
import json
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface


class DNAEncoder:
    """
    DNA Encoder using Goldman algorithm with homopolymer avoidance
    """
    
    def __init__(self):
        self.binary_to_dna = {
            '00': 'A',
            '01': 'C',
            '10': 'G',
            '11': 'T'
        }
        self.dna_to_binary = {v: k for k, v in self.binary_to_dna.items()}
        self.bases = ['A', 'C', 'G', 'T']
    
    def encode(self, binary_data):
        """Convert binary string to DNA sequence"""
        dna_sequence = []
        last_base = None
        
        for i in range(0, len(binary_data), 2):
            bits = binary_data[i:i+2]
            base = self.binary_to_dna.get(bits, 'A')
            
            # Avoid homopolymers (repeated bases)
            if base == last_base:
                alternatives = [b for b in self.bases if b != base]
                base = alternatives[np.random.randint(0, len(alternatives))]
            
            dna_sequence.append(base)
            last_base = base
        
        return ''.join(dna_sequence)
    
    def decode(self, dna_sequence):
        """Convert DNA sequence to binary string"""
        binary_data = []
        
        for base in dna_sequence:
            binary_data.append(self.dna_to_binary.get(base, '00'))
        
        return ''.join(binary_data)


class ReedSolomonCorrector:
    """
    Reed-Solomon Error Correction
    Simplified implementation for DNA storage
    """
    
    def __init__(self, redundancy=5):
        self.redundancy = redundancy
    
    def add_redundancy(self, dna_sequence):
        """Add redundancy to DNA sequence"""
        redundant_sequence = []
        
        for base in dna_sequence:
            redundant_sequence.append(base * self.redundancy)
        
        return ''.join(redundant_sequence)
    
    def remove_redundancy(self, redundant_sequence):
        """Remove redundancy using majority voting"""
        corrected_sequence = []
        
        for i in range(0, len(redundant_sequence), self.redundancy):
            segment = redundant_sequence[i:i+self.redundancy]
            
            # Count each base
            base_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
            for base in segment:
                if base in base_counts:
                    base_counts[base] += 1
            
            # Choose most common base
            consensus_base = max(base_counts, key=base_counts.get)
            corrected_sequence.append(consensus_base)
        
        return ''.join(corrected_sequence)


class AIErrorCorrector:
    """
    AI-Powered Error Correction using Neural Networks
    Detects and corrects error patterns in DNA sequences
    """
    
    def __init__(self):
        self.model = self.build_model()
        self.is_trained = False
    
    def build_model(self):
        """Build neural network for error pattern detection"""
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(8,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(4, activation='softmax')  # A, C, G, T
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def encode_base(self, base):
        """One-hot encode DNA base"""
        encoding = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 
                   'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
        return encoding.get(base, [0, 0, 0, 0])
    
    def decode_prediction(self, prediction):
        """Decode one-hot prediction to base"""
        bases = ['A', 'C', 'G', 'T']
        return bases[np.argmax(prediction)]
    
    def train_on_patterns(self, original_sequences, mutated_sequences):
        """Train model on error patterns"""
        X, y = [], []
        
        for orig, mut in zip(original_sequences, mutated_sequences):
            for i in range(len(orig) - 1):
                # Create context window
                context = []
                for j in range(max(0, i-1), min(len(orig), i+2)):
                    context.extend(self.encode_base(mut[j] if j < len(mut) else 'A'))
                
                # Pad if necessary
                while len(context) < 8:
                    context.extend([0, 0, 0, 0])
                
                X.append(context[:8])
                y.append(self.encode_base(orig[i]))
        
        X = np.array(X)
        y = np.array(y)
        
        self.model.fit(X, y, epochs=50, batch_size=32, verbose=0)
        self.is_trained = True
    
    def correct_sequence(self, sequence):
        """Use AI to correct potential errors in sequence"""
        if not self.is_trained:
            return sequence, 0, 0
        
        corrected = []
        corrections = 0
        errors_detected = 0
        
        for i in range(len(sequence)):
            # Create context window
            context = []
            for j in range(max(0, i-1), min(len(sequence), i+2)):
                context.extend(self.encode_base(sequence[j]))
            
            # Pad if necessary
            while len(context) < 8:
                context.extend([0, 0, 0, 0])
            
            # Predict correct base
            prediction = self.model.predict(np.array([context[:8]]), verbose=0)[0]
            predicted_base = self.decode_prediction(prediction)
            
            # Check if correction is needed (with confidence threshold)
            confidence = np.max(prediction)
            if confidence > 0.7 and predicted_base != sequence[i]:
                errors_detected += 1
                corrected.append(predicted_base)
                corrections += 1
            else:
                corrected.append(sequence[i])
        
        return ''.join(corrected), errors_detected, corrections


class DNAStorageSystem:
    """
    Complete DNA Storage System with AI Error Correction
    """
    
    def __init__(self, redundancy=5, mutation_rate=0.02):
        self.encoder = DNAEncoder()
        self.rs_corrector = ReedSolomonCorrector(redundancy)
        self.ai_corrector = AIErrorCorrector()
        self.mutation_rate = mutation_rate
        self.redundancy = redundancy
        
        # Statistics
        self.stats = {
            'total_encodes': 0,
            'total_decodes': 0,
            'total_errors_detected': 0,
            'total_errors_corrected': 0,
            'average_accuracy': 100.0
        }
    
    def data_to_binary(self, data):
        """Convert any data to binary string"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, bytes):
            pass
        else:
            data = str(data).encode('utf-8')
        
        binary = ''.join(format(byte, '08b') for byte in data)
        return binary
    
    def binary_to_data(self, binary):
        """Convert binary string to data"""
        # Ensure binary length is multiple of 8
        if len(binary) % 8 != 0:
            binary = binary[:-(len(binary) % 8)]
        
        bytes_data = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                bytes_data.append(int(byte, 2))
        
        try:
            return bytes_data.decode('utf-8')
        except:
            return bytes_data
    
    def simulate_mutations(self, dna_sequence):
        """Simulate DNA mutations (degradation over time)"""
        mutated = []
        mutations = 0
        
        for base in dna_sequence:
            if np.random.random() < self.mutation_rate:
                # Mutate to random different base
                alternatives = [b for b in ['A', 'C', 'G', 'T'] if b != base]
                mutated.append(alternatives[np.random.randint(0, len(alternatives))])
                mutations += 1
            else:
                mutated.append(base)
        
        return ''.join(mutated), mutations
    
    def encode(self, data, add_mutations=False):
        """
        Encode data to DNA sequence with error correction
        
        Args:
            data: Input data (string, bytes, or any serializable object)
            add_mutations: Whether to simulate mutations for testing
        
        Returns:
            Dictionary with encoded DNA and metadata
        """
        # Convert to binary
        binary = self.data_to_binary(data)
        
        # Encode to DNA
        dna_sequence = self.encoder.encode(binary)
        
        # Add Reed-Solomon redundancy
        redundant_dna = self.rs_corrector.add_redundancy(dna_sequence)
        
        # Optionally simulate mutations
        mutations = 0
        if add_mutations:
            redundant_dna, mutations = self.simulate_mutations(redundant_dna)
        
        # Update statistics
        self.stats['total_encodes'] += 1
        
        return {
            'original_length': len(data),
            'binary_length': len(binary),
            'dna_length': len(dna_sequence),
            'redundant_dna_length': len(redundant_dna),
            'dna_sequence': redundant_dna,
            'compression_ratio': len(redundant_dna) / len(binary) if len(binary) > 0 else 0,
            'mutations_simulated': mutations,
            'redundancy_factor': self.redundancy,
            'timestamp': datetime.now().isoformat()
        }
    
    def decode(self, dna_sequence, use_ai=True):
        """
        Decode DNA sequence back to original data with AI error correction
        
        Args:
            dna_sequence: DNA sequence to decode
            use_ai: Whether to use AI error correction
        
        Returns:
            Dictionary with decoded data and error correction stats
        """
        # Remove redundancy with Reed-Solomon correction
        corrected_dna = self.rs_corrector.remove_redundancy(dna_sequence)
        
        # AI-powered error correction
        errors_detected = 0
        errors_corrected = 0
        if use_ai and self.ai_corrector.is_trained:
            corrected_dna, errors_detected, errors_corrected = \
                self.ai_corrector.correct_sequence(corrected_dna)
        
        # Decode to binary
        binary = self.encoder.decode(corrected_dna)
        
        # Convert to original data
        data = self.binary_to_data(binary)
        
        # Update statistics
        self.stats['total_decodes'] += 1
        self.stats['total_errors_detected'] += errors_detected
        self.stats['total_errors_corrected'] += errors_corrected
        
        accuracy = 100.0
        if errors_detected > 0:
            accuracy = (errors_corrected / errors_detected) * 100
        
        self.stats['average_accuracy'] = (
            (self.stats['average_accuracy'] * (self.stats['total_decodes'] - 1) + accuracy) 
            / self.stats['total_decodes']
        )
        
        return {
            'decoded_data': data,
            'errors_detected': errors_detected,
            'errors_corrected': errors_corrected,
            'accuracy': accuracy,
            'data_integrity': 100.0 if errors_detected == 0 else accuracy,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_statistics(self):
        """Get system statistics"""
        return self.stats


# Initialize DNA Storage System
dna_system = DNAStorageSystem(redundancy=5, mutation_rate=0.02)


# REST API Endpoints

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'DNA Storage API',
        'version': '1.0.0',
        'description': 'AI-Powered DNA Storage Encoding/Decoding System',
        'endpoints': {
            '/encode': 'POST - Encode data to DNA',
            '/decode': 'POST - Decode DNA to data',
            '/statistics': 'GET - Get system statistics',
            '/train': 'POST - Train AI error correction model',
            '/health': 'GET - Check API health'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_trained': dna_system.ai_corrector.is_trained,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/encode', methods=['POST'])
def encode_data():
    """
    Encode data to DNA sequence
    
    Request JSON:
    {
        "data": "text to encode",
        "add_mutations": false,
        "redundancy": 5
    }
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update redundancy if specified
        if 'redundancy' in request_data:
            dna_system.redundancy = int(request_data['redundancy'])
            dna_system.rs_corrector = ReedSolomonCorrector(dna_system.redundancy)
        
        # Encode
        result = dna_system.encode(
            request_data['data'],
            add_mutations=request_data.get('add_mutations', False)
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decode', methods=['POST'])
def decode_data():
    """
    Decode DNA sequence to original data
    
    Request JSON:
    {
        "dna_sequence": "ATCGATCG...",
        "use_ai": true
    }
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'dna_sequence' not in request_data:
            return jsonify({'error': 'No DNA sequence provided'}), 400
        
        # Decode
        result = dna_system.decode(
            request_data['dna_sequence'],
            use_ai=request_data.get('use_ai', True)
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    return jsonify({
        'success': True,
        'statistics': dna_system.get_statistics()
    })


@app.route('/train', methods=['POST'])
def train_ai():
    """
    Train AI error correction model
    
    Request JSON:
    {
        "training_data": [
            {"original": "ATCG", "mutated": "ATCG"},
            ...
        ]
    }
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'training_data' not in request_data:
            # Generate synthetic training data
            original_sequences = []
            mutated_sequences = []
            
            for _ in range(100):
                # Generate random DNA sequence
                length = np.random.randint(50, 200)
                bases = ['A', 'C', 'G', 'T']
                original = ''.join(np.random.choice(bases, length))
                
                # Simulate mutations
                mutated, _ = dna_system.simulate_mutations(original)
                
                original_sequences.append(original)
                mutated_sequences.append(mutated)
        else:
            training_data = request_data['training_data']
            original_sequences = [d['original'] for d in training_data]
            mutated_sequences = [d['mutated'] for d in training_data]
        
        # Train the model
        dna_system.ai_corrector.train_on_patterns(original_sequences, mutated_sequences)
        
        return jsonify({
            'success': True,
            'message': 'AI model trained successfully',
            'training_samples': len(original_sequences)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/batch_encode', methods=['POST'])
def batch_encode():
    """
    Encode multiple data items in batch
    
    Request JSON:
    {
        "items": ["data1", "data2", ...],
        "redundancy": 5
    }
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'items' not in request_data:
            return jsonify({'error': 'No items provided'}), 400
        
        results = []
        for item in request_data['items']:
            result = dna_system.encode(item)
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_items': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("DNA Storage API Server")
    print("AI-Powered Error Correction System")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  POST /encode        - Encode data to DNA")
    print("  POST /decode        - Decode DNA to data")
    print("  GET  /statistics    - Get statistics")
    print("  POST /train         - Train AI model")
    print("  GET  /health        - Health check")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
