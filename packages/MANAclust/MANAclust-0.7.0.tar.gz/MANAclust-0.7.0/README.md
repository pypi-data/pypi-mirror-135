![MANAclust|756x240,5%](logo_V1.jpg)

### Merged Affinity Network Association clustering ###

### About ###
* MANAclust helps to identify subtypes of diseases by integration of medical records and multi-omics
* It takes in categorical and numeric datasets that you want to use for joint unsupervised clustering to identify subgroups
* Then it does upsupervised feature selection using an information theory driven algorithm for categorical variables and looks for negative correlations for numeric variables
* Next MANAclust calculates normalized affinity matrices for each of the input datasets
* MANAclust then merges the affinity matrices from your datasets into a final affinity matrix which is then used for clustering
* MANAclust's clustering algorithm is a new clustering algorithm that combines the strengths and weaknesses of Louvain modularity and affinity propagation
* MANAclust then goes through all of the clusters comparing them to each other by each dataset, doing Chi-square or ANOVAs for categorical and numeric datasets respectively. For globally significant features, post-hocs are also performed to identify the individual differences between all of the sample groups.

### How do I get set up? ###

```
python3 -m pip install manaclust
```
Note that you might have to use sudo for this command depending on if you're doing a global or local installation.

### How do I use MANAclust? ###

* You basically just need to tell MANAclust where your categorical (-cat) and numeric (-num) dataset files are. Note that these have to be in tab-delimited text file format.
* You can also give it files that you want to use to evaluate the efficacy of clustering. For example, if you have diagnoses that you want to use, but don't want MANAclust to actually do clustering on, you can feed that into the -test_cat argument. Similarly for any numeric values you don't want used for clustering, but want to look for differences in (-test_num).
* The basic syntax is:

```
python3 -m mana_clust.mana_clust -cat <path_to_categorical_dataset_1.tsv> \
                                      <path_to_categorical_dataset_2.tsv> \
							     -num <path_to_numeric_dataset_1.tsv> \
								      <path_to_numeric_dataset_2.tsv> \
							     -test_cat <path_to_categorical_dataset_not_used_for_clustering.tsv> \
								 -test_num <path_to_numeric_dataset_not_used_for_clustering.tsv> \
								 -out_dir <path_to_the_output_directory>

```

* Included in this repository are some dummy files for you to test things out with. You can make sure everything is up and running by using these files with the syntax below:

```
python3 -m mana_clust.mana_clust -cat ~/Downloads/manaclust/test/categorical_data_file_0.tsv \
							     -num ~/Downloads/manaclust/test/numeric_data_file_0.tsv \
								      ~/Downloads/manaclust/test/numeric_data_file_0.tsv \
							     -test_cat <path_to_categorical_dataset_not_used_for_clustering.tsv> \
								 -test_num <path_to_numeric_dataset_not_used_for_clustering.tsv> \
								 -out_dir ~/Downloads/manaclust/test/out/
```

### How do I use my own datasets? ###
* MANAclust takes in either categorical or numeric datasets.
* Both categorical and numeric datasets: must be in tab delimited formats.
* Categorical datasets formats: As is traditional in small categorical datasets for medical records, categoical datasets are assumed to have each row as a subject, and each column as a variable. 
* Numeric datasets formats: As is traditional for large omic datasets, the features (genes or similar) are assumed to be in rows, while the subjects are in columns.
* Subjects that are missing from a dataset: That's fine! Given the reality of clinical datasets, we intentinally designed the MANAclust program to be able to handle missing data in every way. 
* Does the order of the subjects matter in the datasets?: Nope - the subjects can be in any order in all of your datasets, MANAclust will piece everything together correctly
* Missing values in categorical datasets: That's fine! As long as the missing values are noted with a single notation (i.e.: "N/A"), you can give this as an argument to MANAclust using the -MD argument (which stands for missing_data).
* Mixed categorical/numeric datasets: should be fed in as categorical datasets. Any variables that have float/int values will automatically be digitized into bins such that they can be treated as categorical variables. Note this drawback however: numeric variables will be treated as categorical. This could result in power loss, but will also enable the detection of non-monotonic patterns. In theory an entirely numeric dataset could also be given 

### How do I interpret the output? ###
* MANAclust generates an html file that gives you a walk through of all the figures and analyses that MANAclust performs. Simply open up the "MANAclust_summary.html" file and start exploring!

### How can I dig into the data further? ###
* MANAclust also generates a meta_ome_results.pkl file. This object saves all the nitty gritty aspects of the analysis that you can explore interactively. Just start print out the object & you'll see documentation of everything that might be of interest.


```
from mana_clust.common_functions import import_dict
from mana_clust.mana_clust import cluster_omes
from mana_clust.mana_cat import feature, categorical_ome
from mana_clust.mana_continuous import num_ome

meta_ome = import_dict('<path/to/meta_ome_results.pkl>' )

print(meta_ome)
```

* To look at a specific input dataset, you can print out the objects in the meta_ome.cat_omes and meta_ome.num_omes lists:

```
print(meta_ome.cat_omes[0])

print(meta_ome.num_omes[0])
```




### Who do I talk to? ###

* Scott Tyler: scottyler89@gmail.com
