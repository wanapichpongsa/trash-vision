# Why Attention Is All You Need

**Attention Pipeline**
1. Words and tokens -> Vectors a.k.a Input Embeddings to then compute attention weights.
2. Positional encoding since transformers lack recurrence.
3. Self-attention mechanism (see above).
4. Multi-head Attention to capture multiple contextual features.
5. Feed-forward layer: Position-wise fully connected layer and activation (ReLU).
6. Residual connection and layer normalization: maintain gradient flow and stabilize training.
7. Stacking Layers: Repeat the attention and feed-forward layers to learn complex patterns.
8. Output Layer: Use a softmax layer for classification or generation confidence scores sum up to 1.

**Efficiency**
1. Parallel computation unlike RNNs.
2. Captures global context better than CNNs.
3. Generalised -> Can perform many tasks e.g., translation, summarisation, and vision.

## Low Abstraction Example

### 1. Input Embeddings
$$E = X \cdot W_E$$

```python
import numpy as np

# Hyperparameters
vocab_size = 10000  # Vocabulary size
d_model = 512       # Embedding dimension
seq_len = 100       # Sequence length
batch_size = 32     # Batch size

# Randomly initialized embedding matrix
W_E = np.random.randn(vocab_size, d_model)

# Example Input: One-hot encoded tokens (Batch Size, Sequence Length)
X = np.random.randint(0, vocab_size, (batch_size, seq_len))

# Input Embedding
E = np.array([[W_E[token] for token in seq] for seq in X])  # Shape: (Batch Size, Seq Length, d_model)
```

### 2. Positional Encoding

**Even Index (Sin Componenet)**
$$PE_{pos, 2i} = \sin\left(\frac{pos}{10000^{\frac{2i}{d_{model}}}}\right)$$

**Odd Index (Cosine Component)**
$$PE_{pos, 2i+1} = \cos\left(\frac{pos}{10000^{\frac{2i}{d_{model}}}}\right)$$

```python
# Positional Encoding Matrix
PE = np.zeros((seq_len, d_model))

for pos in range(seq_len):
    for i in range(0, d_model, 2):
        angle = pos / (10000 ** ((2 * i) / d_model))
        PE[pos, i] = np.sin(angle)
        PE[pos, i + 1] = np.cos(angle)

# Broadcasting addition
E = E + PE  # Add positional encoding to input embeddings
```

### 3. Self-Attention

**Generate Q, K, and V**
$$Q = E \cdot W_Q, \quad K = E \cdot W_K, \quad V = E \cdot W_V$$

**Scaled Dot-Product Attention**
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

```python
# Weight matrices for Q, K, V
W_Q = np.random.randn(d_model, d_model)
W_K = np.random.randn(d_model, d_model)
W_V = np.random.randn(d_model, d_model)

# Calculate Q, K, V
Q = np.matmul(E, W_Q)  # Shape: (Batch Size, Seq Length, d_model)
K = np.matmul(E, W_K)
V = np.matmul(E, W_V)

# Scaled Dot-Product Attention
d_k = d_model
attention_scores = np.matmul(Q, K.transpose(0, 2, 1)) / np.sqrt(d_k)  # Shape: (Batch Size, Seq Length, Seq Length)

# Softmax for Attention Weights
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

attention_weights = softmax(attention_scores)

# Multiply Attention Weights with V
attention_output = np.matmul(attention_weights, V)  # Shape: (Batch Size, Seq Length, d_model)
```

### 4. Multi-Head Attention
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) \cdot W_O$$

```python
num_heads = 8
head_dim = d_model // num_heads

# Splitting Q, K, V into multiple heads
Q_heads = Q.reshape(batch_size, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)
K_heads = K.reshape(batch_size, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)
V_heads = V.reshape(batch_size, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)

# Calculate Attention for each head
attention_output_heads = np.matmul(Q_heads, K_heads.transpose(0, 1, 3, 2)) / np.sqrt(head_dim)
attention_weights_heads = softmax(attention_output_heads)
attention_heads = np.matmul(attention_weights_heads, V_heads)

# Concatenate heads and project output
attention_output = attention_heads.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, d_model)
W_O = np.random.randn(d_model, d_model)
multi_head_output = np.matmul(attention_output, W_O)
```

### 5. Feed-Forward Network

$$\text{FFN}(x) = \text{ReLU}(x \cdot W_1 + b_1) \cdot W_2 + b_2$$

```python
d_ff = 2048

# Feed-Forward Network Weights
W_1 = np.random.randn(d_model, d_ff)
b_1 = np.random.randn(d_ff)
W_2 = np.random.randn(d_ff, d_model)
b_2 = np.random.randn(d_model)

# Feed-Forward Calculation
def relu(x):
    return np.maximum(0, x)

ffn_output = relu(np.matmul(multi_head_output, W_1) + b_1)
ffn_output = np.matmul(ffn_output, W_2) + b_2
```

### 6. Residual Connection and Layer Normalisation

**Residual Connection**
$$\text{Output} = x + \text{SubLayer}(x)$$

**Layer Normalisation**
$$\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$$

```python
epsilon = 1e-6

# Residual Connection
residual_output = multi_head_output + ffn_output

# Layer Normalization
mean = np.mean(residual_output, axis=-1, keepdims=True)
std = np.std(residual_output, axis=-1, keepdims=True)
normalized_output = (residual_output - mean) / (std + epsilon)
```
### 7. Stackign Layers
**Encoding Layer**
1. Scaled Dot-Product Attention
2. Residual Connection and Layer Normalization:
$$\text{Output}_1 = \text{LayerNorm}(X + \text{Attention}(Q, K, V))$$
3. Feed-Forward Network
4. Second Residual Connection and Layer Normalization:
$$\text{Encoder Output} = \text{Encoder Layer}_N(...\text{Encoder Layer}_2(\text{Encoder Layer}_1(X))...)$$

**Stacking Encoder Layers**
$$\text{Encoder Output} = \text{Encoder Layer}_N(...\text{Encoder Layer}_2(\text{Encoder Layer}_1(X))...)$$

```python
def encoder_layer(X):
    # Multi-Head Attention + Residual + LayerNorm
    attention_output = multi_head_attention(X)
    X = layer_norm(X + attention_output)
    
    # Feed-Forward + Residual + LayerNorm
    ffn_output = feed_forward(X)
    X = layer_norm(X + ffn_output)
    
    return X

def encoder_stack(X, num_layers=6):
    for _ in range(num_layers):
        X = encoder_layer(X)  # Pass output through each Encoder Layer
    
    return X

# EXPECTED OUTPUT -> Encoder Output Shape: (32, 100, 512)
```

### 8. Softmax Output Layer

$$\text{Softmax}(z_i) = \frac{\exp(z_i)}{\sum_{j} \exp(z_j)}$$

#TODO: Code softmax function
```python
# Output Layer Weights
W_out = np.random.randn(d_model, vocab_size)

# Classification Output
logits = np.matmul(normalized_output, W_out)
output = softmax(logits)
```