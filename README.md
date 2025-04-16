# Heron Coding Challenge - File Classifier - Jake Crouchley

## Overview

### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?

Since the original classifier was based on filenames, it required strict file naming and a degree of pre-processing of any files that weren't provided well-named.

Because the logic was fairly simple, there wasn't a huge need for much supporting classes and helpers functions, but as complexity was added I've structured classes to help condense the file validation logic in one place. I've chosen to make a distinction between Unprocessed and Processed files, to differentiate between the two states since the 'processing' of extracting text might not be something you would want to do immediately, particularly if the project is extended to support batch requests.

- How might you extend the classifier with additional technologies, capabilities, or features?

My approach was to leverage pre-trained models that can provide semantic similarity to class labels, but also with some degree of basic fine-tuning through an additional comparison with keywords.

I originally looked into zero shot classification with a larger-sized model but the results without any fine-tuning were sub-par after some manual testing. Instead, I went with SentenceTransformers and a keyword-based comparison that provided a higher degree of accuracy with a much smaller model required.

Further improvements would be to train or fine-tune a model directly from data that Heron has available in order to reach a higher level of accuracy. In terms of testing, it would be good to cover expected cases of classification and ensuring the threshold is valid, for example.

### Part 2: Productionising the Classifier

- How can you ensure the classifier is robust and reliable in a production environment?

By using Docker we can ensure that the classifier is easily replicated in different environments, and can easily be deployed via a number of cloud options.

Missing feature: running a production server instance, currently the application still runs with the development server.

- How can you deploy the classifier to make it accessible to other services and users?

I integrated the project with a CI/CD pipeline in Github Actions that builds and uploads the Dockerised container to ECR and ECS. This could be deployed with a load balancer and an API gateway to provide a scalable and accessible means of access to the service.

Missing feature: opportunities for better caching behaviour in the install step.

## Getting Started (unchanged)

1. Clone the repository:

   ```shell
   git clone <repository_url>
   cd heron_classifier
   ```

2. Install dependencies:

   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the Flask app:

   ```shell
   python -m src.app
   ```

4. Test the classifier using a tool like curl:

   ```shell
   curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
   ```

5. Run tests:
   ```shell
    pytest
   ```
