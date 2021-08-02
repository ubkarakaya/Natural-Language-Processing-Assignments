
import analogy
import classification_doc as cd

'''# TASK 1: ANALOGY
words = analogy.read_relations("word-test.v1.txt")
# Load the pre-trained model to analogy
model = analogy.load_model("GoogleNews-vectors-negative300.bin")
analogy.prediction(model, words)'''

# TASK 2: DOCUMENT CLASSIFICATION
accuracies = []
train_df, test_df = cd.read_parse("tagged_plots_movielens.csv")
model, train_documents = cd.generate_model(train_df)
model_v, test_documents = cd.generate_model(test_df)

for i in range(5):
    # Evaluation of the model
    accuracies.append(cd.evaluation(model, train_documents, test_documents))
print("Maximum value of the accuracy is "+str(max(accuracies))+" %")
