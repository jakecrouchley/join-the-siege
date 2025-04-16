Approach:

- Find a pre-trained model
- Use that to classify document contents based on labels
- Add tests to cover cases like new labels
- Extract logic out to make it more extensible
- Add CI/CD, probably Dockerised and deployed to AWS

Choice of approach:

- ~~Zero-shot classification~~
  - ~~Chosen because it allows a more straightforward implementation~~
  - ~~Allows for dynamic labelling, allowing scaling to other industries, at the cost of lower accuracy and no opportunity to fine-tune~~
- Model size was large, and didn't allow easy fine-tuning, so decided to use SentenceTransformers
  - faster classification
  - more ability to do basic fine-tuning
  - more semantic similarity
  - smaller model size

Missing features:

- Investigate caching to determine whether pip packages can be cached in GitHub actions
- More tests to cover outcomes of classification
-
