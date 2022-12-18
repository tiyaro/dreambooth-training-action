# DreamBooth Training Action

This is a template repo for **training and publishing your own custom [Stable Diffusion Dreambooth](https://console.tiyaro.ai/explore/dreambooth-base/) model** using Tiyaro and GitHub Actions.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lq8df7smjtzb3w6wekvx.jpg)

## Requirements

- Tiyaro account with one of the paid plans [Tiyaro Pricing](https://www.tiyaro.ai/pricing/)
- A few training images.  This repo has a few already [data](./data/) directory

## Training the model

1. Create your own copy of this repository by clicking the green `Use this template` button, then `Create a new repository`. Name your repository, and choose visibility.  You could also `fork` or [import](https://github.com/new/import) this repository.
1. Add your own or re-use puppy images in the [data](./data) directory.
1. Commit your changes to git and push to your main branch on GitHub.
1. Copy your Tiyaro API Key from [console.tiyaro.ai/apikeys](https://console.tiyaro.ai/apikeys) and [create a repository secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `TIYARO_API_TOKEN`.
1. Trigger the workflow from your GitHub repo page: `Actions` > `Train a model` > `Run workflow`.
1. The training process takes 20-40 minutes to run.  You'll receive an email with status and details.

## Running the model

You can also see the status of your job in [Tiyaro Model Studio](https://console.tiyaro.ai/modelstudio-train)

Clicking on your `<dreambooth-model-name>` in `Results` -> `TrainedModels` will take you to your custom model card.

The custom model card is similar to any other model hosted as API with the API url, sample code, demo etc.  You can evaluate your dreambooth model using Tiyaro demo from the UI or by using Tiyaro Inference API.

Tiyaro [Dreambooth Training API](https://tiyaro-api.readthedocs-hosted.com/en/latest/dreambooth.html#id3) has lots of parameters allowing good customizability and fine-tuning.  This action template is powered by script [main.py](./main.py) that just requires mandatory input parameters.  One can extend this script to provide more params.

If you have questions, feel free to open an issue or reachout to us at help@tiyaro.ai.

## Blog
- https://www.tiyaro.ai/blog/dreambooth-retraining/

## API Docs
- https://tiyaro-api.readthedocs-hosted.com/en/latest/dreambooth.html
