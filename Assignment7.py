import numpy as np

"""
ASSIGNMENT-7
Training Set Reduction through k-nearest neighbour

You are given a set of d-dimensional data points along with their labels. You goal
is to reduce the training set size so that you can improve the prediction time. To
that goal, you need to implement the following algorithm.

1. Initialize subset S with a single training example
2. Classify all remaining samples using the subset S (apply 1-nn rule)
3. Transfer any incorrectly classified samples to the subset S
4. Return to 2 until S does not change
5. S will be the final compressed set.

Input format: Your program will take the file with the sentences as the input.
Output: It will produce output on an output file named assignment-7-out.txt
"""

class TrainingSetReducer:
    def __init__(self):
        self.features = []
        self.n_samples = 0
        self.n_dimensions = 0

    def fetch_dataset(self, filename):
        """
        Read the dataset file and store in dictionary
        """
        dict = {}
        self.features = []
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.n_samples = len(lines) - 1     # excluding the header
            for line in lines:
                line = line.strip()
                if len(dict) == 0:
                    line = line[1:]      # ignore '#' at the start
                list = line.split(',')
                if len(dict) == 0:
                    # build keys   
                    for key in list:
                        dict[key] = []
                        self.features.append(key)
                    self.n_dimensions = len(self.features) - 1    # excluding the class labels
                else:
                    # add sample-wise values
                    for i, val in enumerate(list):
                        dict[self.features[i]].append(float(val))

        # convert class labels to int
        dict['class'] = [int(val) for val in dict['class']]
        return dict
    
    def write_output(self, filename, dict):
        """
        Write-back the data from dictionary into a new text file
        """
        with open(filename, 'w') as file:
            # write header
            header = "#" + ",".join(self.features)
            file.write(header + '\n')

            # write samples
            count = len(dict['class'])
            for i in range(count):
                line = ",".join(str(dict[key][i]) for key in self.features)
                file.write(line + '\n')

    def predict(self, train_set, test_sample):
        """
        Predict on the test_sample using 1-KNN from train_set
        i.e. assign the class label of the closest train_sample
        """
        min_dist = np.inf
        pred_class = None

        for sample in train_set:
            curr_dist = np.sum([(test_sample[i] - sample[i])**2 for i in range(self.n_dimensions)])
            if curr_dist < min_dist:
                pred_class = sample[-1]
                min_dist = curr_dist
        return pred_class

    def reduce_training_set(self, input_filename, output_filename):
        """
        Reduce the training dataset using KNN at K=1
        """
        data = self.fetch_dataset(input_filename)

        # Step-1: Initialize a set S with one sample from the dataset
        s = set()
        first_sample = tuple([data[key][0] for key in self.features])
        s.add(first_sample)
        
        # store remaining samples
        samples_remaining = []
        for i in range(1, self.n_samples):
            sample = tuple([data[key][i] for key in self.features])
            samples_remaining.append(sample)

        iter = 0
        while True:
            incorrect = set()
            
            # Step-2: Classify remaining samples using 1-NN
            for sample in samples_remaining:
                pred_class = self.predict(s, sample)
                if pred_class != sample[-1]:
                    incorrect.add(sample)    
            print(f"Iteration {iter}: S = {len(s)}, Remaining samples = {len(samples_remaining)}, Incorrect = {len(incorrect)}")

            # Step-3: Transfer incorrectly classified samples to S
            s.update(incorrect)
            # remove the transferred samples from remaining samples
            for sample in incorrect:
                samples_remaining.remove(sample)
            
            # Step-4: Stop if the set S remains unchanged
            if (len(incorrect) == 0):
                break
            iter += 1
            
        # Step-5: S contains the final compressed dataset
        reduced_data = {key : [] for key in self.features}
        for sample in s:
            for i, key in enumerate(self.features):
                reduced_data[key].append(sample[i])
        
        # write the reduced dataset to output file & return its length
        self.write_output(output_filename, reduced_data)
        return len(s)


if __name__ == "__main__":
    tsr = TrainingSetReducer()
    try:
        reduced_count = tsr.reduce_training_set('files/assn-07-data.txt', 'files/assignment-7-out.txt')
        original_count = tsr.n_samples
        compression_rate = (original_count - reduced_count) / original_count * 100
        
        print("Training dataset compressed successfully!")
        print(f"Count of samples: before = {tsr.n_samples}, after = {reduced_count}")
        print(f"Compression rate = {compression_rate:.2f}%")
    except Exception as e:
        print("ERROR in compressing the dataset!")
        print(e)
