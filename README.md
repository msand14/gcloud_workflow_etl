# Google Cloud workflow for ETL orchestration

## Index
1. [Description](#id1)
2. [Technology stack](#id2)

    2.1. [Google Cloud Platform](#id21)

    2.2. [Github](#id22)

    2.3. [Pyspark](#id23)

    2.4. [Bash](#id24)

3. [Steps](#id3)

    3.1. [Set up GCP](#id31)

    3.2. [Set up Github](#id32)
    
    3.3. [Github Actions](#id33)

## 1.   Description<a name="id1"></a>
This project consists a demostration of how an ETL (Extraction Transformation and Load) can be done within Google Cloud using different tools/technologies/languages.

Google Cloud has been chosen for this project because its easy to get a free account a take advantage of its compute power.

The aim of the ETL is to get ingest data files from a famous [Kaggle Youtube statistics dataset](https://www.kaggle.com/datasets/datasnaek/youtube-new) and with the idea of the 3 layers ( raw, silver and gold) structure taken from the Lakehouse Architecture get tables with proper quality we can afterwards explore with Big Query and also create some dashboards.

The dataset contains the statistics of videos from different countries and also information regarding the different categories each of the videos can be classified in.

## 2. Technology stack<a name="id2"></a>

### 2.1 Google Cloud Platform<a name="id21"></a>
-   **Google Cloud Storage**: Used for saving initially the youtube files from Kaggle and also for saving the different parquet files derived from the different stages of the ETL

-   **Google Dataproc**: Used for computing the ETL workflow.

### 2.2 Github<a name="id22"></a>
CI/CD of the ETL code and for the Dataproc Workflow template

### 2.3 Pyspark<a name="id23"></a>
Used for performing in a distributed way the ETL transformations between the different workers of the cluster and because of that cut down the proccessing time.

### 2.4 Bash<a name="id24"></a>
Just for some commands in the yaml files that contains the operations to perform in Github Actions

## 3.  Steps<a name="id3"></a>

### 3.1.   Set up GCP<a name="id31"></a>

First of all, create a [free account](https://cloud.google.com/?hl=en) in Google Cloud Platform

Create a project

Go to Google Cloud Storage and create 1 bucket

Inside of the created bucket, create 4 folders, one per layer with the default configuration:
- raw
- bronze
- silver
- gold

Inside of each of the **first three folders ( rar, bronze and silver)**  create 2 subfolders. For example in the raw bucket it will be like this:
- videos
- categories

The structure of our bucket should look like this:
- raw
    - videos
    - categories
- bronze
    - videos
    - categories
- silver
    - videos
    - categories
- gold


Create a Service Account (IAM/Service Accounts on the lateral tab) to allow Github actions to connect with Google Cloud. We will explain later with more details why we use Github actions.

Go to your recently created Service Account  and navigate to keys. Create a new key in a json format ( it will be downloaded)

Now, inside your Service Account  you should see some details, including the email. Copy that email and go back to your bucket. Go to the permissions tab of the bucket and click over Grant Access. In *"New principals"* paste the Service Account email and in the text box below select the following role: *Storage Object Admin*.

Wit the previous step we ensure that the Service account we will use from Github will be allowed to access our GCS bucket.


### 3.2. Set up Github<a name="id32"></a>

We will use Github to save our code and work in a CI environment. Also there, we will use the CD part to deploy with the help of [Github Actions](https://github.com/features/actions) the last version of our code and also to run the ETL job from there.

Lets start creating a repository

Inside of your repository go to *Settings* and on the left menu go to Secrets and variables in the Security section. Once there click on *Actions*.

We are creating here two secrets:
- GCP_SA_EMAIL: Here we paste the the Service Account's email from Google Cloud Platform mentioned in the previous section 3.1.
- GCP_SA_KEY: Paste the code of the Service Account's key (JSON file downloaded in Section 3.1)


### 3.3. Github Actions <a name="id33"></a>

In this project we are performing automatically some operations. In order this operations to be detected by Github and to be run automatically by an agent, it's necessary to create a proper structure for the file in our code that will contain the action/operation. The following folders need to be created from the root of our project:

        .github/workflows/
Once created this folders, inside */workflows* we create the yaml file that contains the action information:

-   deploy-dataproc-workflow-template.yaml

    1. The action will be triggered whenever we push to *main* branch.
    2. Configured google-github-actions/auth for GCP authentication.
    3. Configured google-github-actions/setup-gcloud for interacting with GCP SDK afterwards.
    4. Delete the existent workflow template in Google Dataproc.
    5. Create an empty workflow template with a given name.
    6. Fill in the template from step 5 with repo file template yaml.
    7. Run ( its not neccessary that the workflow template is created in GCP) a repo file yaml as a job in Google Cloud Dataproc

-   deploy-code-to-GCS.yaml

    1. The action will be triggered whenever we push to *main* branch.
    2. Configured google-github-actions/auth for GCP authentication.
    3. Configured google-github-actions/setup-gcloud for interacting with GCP SDK afterwards.
    4. Remove everyhting contained inside the GCS bucket (ETL files) but the source files.
    5. Copy from the repo the updated ETL files.

Next time we push the code to main branch, Github actions will run two jobs or actions.

