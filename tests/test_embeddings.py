from retrieval.embeddings import embed_text, embed_batch

# Test single embedding
v = embed_text("hello world")
print(type(v))
print(v.shape)
print(v.dtype)
print(v[:5])

# Test batch
vs = embed_batch(["hello", "world"])
print(vs.shape)