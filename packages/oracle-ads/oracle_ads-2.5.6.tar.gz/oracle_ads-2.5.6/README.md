# Overview

The Oracle Accelerated Data Science (ADS) SDK is maintained by the Oracle Data Science team. Its goal is to speed up common data science activities. It does this by providing tools that automate or simplify common tasks that a data scientist performs. It also provides a data scientist-friendly interface to Oracle Cloud Infrastructure (OCI) web services.

ADS allows you to store your data on Oracle Object Storage and read it into Pandas, natively. Use ADS to automate data transformation or get recommendations on what transformations will improve your models. Use Feature Types to create features that have multiple inheritances and are not bound by the restrictions of the data type. Use this to create reusable summary statistics, summary plots, validate the data, looking for potential problems, and select features based on their type. Use the ADSTuner to perform smart hyperparameter tuning operations. The text extraction module takes the hard work out of extracting text from various document formats so that you can quickly get to NLP modeling.

Integration with OCIs services is a key feature of ADS. The integrations are focused on the use cases that data scientists need. For example, the Vault service allows you to store secrets. ADS simplifies the process by taking a dictionary, say username and password, and it will return a dictionary. There are integrations to the Data Science services such as Projects, Module Catalog, Model Deployment, and Jobs. But it also has integrations to other services that data scientists commonly use such as the Vault, Autonomous Database, Object Storage and much more.

Contributions are welcome.

# Installation 

You have various options when installing ADS package. 

* Installing the base package of oracle-ads

```
pip install oracle-ads
```


* Installing extras libraries

If you would use ADS within a notebook session, install 
```
pip install oracle-ads[notebook]
```

If you would work on machine learning tasks, install
```
pip install oracle-ads[boosted]
```

If you would work on text related tasks, install
```
pip install oracle-ads[text]
```

If you need support for a broad set of data formats (for example, excel, avro, etc.), install
```
pip install oracle-ads[data]
```

**Note** 

- Multiple extra dependencies can be installed together, for example,
```
pip install oracle-ads[notebook,boosted,text]
```
