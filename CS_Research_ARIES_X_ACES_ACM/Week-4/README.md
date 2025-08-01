# Brain Tumor Detection with CNNs - CSoT'25 Week 4 Project

## Introduction

Welcome to Week 4 of the CSoT'25 CS Research program by ARIES x ACES ACM! This week, we apply Convolutional Neural Networks (CNNs) to a real-world challenge: detecting brain tumors from MRI scans. You'll build a complete deep learning workflow, from data preprocessing to model evaluation, resulting in a functional classification model.

## Goal and Learning Objectives

The goal is to create a binary classification model to detect brain tumors in MRI scans. By completing this project, you will:

- Process and prepare a raw dataset.
- Implement and train a CNN using TensorFlow/Keras.
- Evaluate model performance and visualize results.
- Gain hands-on experience with a real-world medical imaging application.

## Dataset

The **Brain MRI Dataset for Tumor Detection** is used for this project. Key details:

- **Content**: Two folders:
  - `yes`: MRI scans of brains with tumors.
  - `no`: MRI scans of brains without tumors.
- **Format**: Standard image files (.jpg or .png).
- **Significance**: A classic dataset for binary image classification, with applications in medical diagnostics.
- **Access**: [Link to the dataset](https://www.kaggle.com/datasets/sudipde25/mri-dataset-for-detection-and-analysis/data)

## Tasks

1. **Environment Setup and Data Exploration**

   - Set up a Colab or Jupyter Notebook.
   - Download the dataset and load images from the `yes` and `no` folders.
   - Visualize sample images from each class to understand the data.

2. **Data Preprocessing**

   - Resize images to a uniform size (e.g., 150x150 pixels).
   - Normalize pixel values.
   - Assign numerical labels (1 for tumor, 0 for no tumor).
   - Split the dataset into 80% training and 20% testing.

3. **Model Building and Training**

   - Use TensorFlow/Keras to create a sequential CNN with convolutional, pooling, and dense layers, ending with a sigmoid activation.
   - Compile the model.
   - Train the model using the `fit` method with training and validation data for a set number of epochs.

4. **Model Evaluation**
   - Plot accuracy and loss curves from the model's training history.
   - Evaluate the model on the test set using the `evaluate` method to obtain the final accuracy score.

## Submission Guidelines

- **What to Submit**: A single link to your Google Colab or Jupyter Notebook.
- **Accessibility**: Ensure the link is publicly accessible. In Google Colab, set "General access" to "Anyone with the link" via the "Share" option.
- **Notebook Requirements**:
  - Clean, well-commented code with all cell outputs.
  - Clearly display the final test accuracy score.
- **Submission Form**: [Submit here!!](https://docs.google.com/forms/d/e/1FAIpQLSfTv8HNTAIdrZ31FiGeS-uv2f7qscx5dAnUjVrupxlbhFL17A/viewform?usp=sharing&ouid=115413717050185681699)

## Optional Challenges

For those eager to go further:

- **Data Augmentation**: Use Keras’ `ImageDataGenerator` to apply random transformations (e.g., rotations, zooms, flips) to improve model generalization and reduce overfitting.
- **Architecture Experimentation**: Modify the CNN by adding more `Conv2D` layers or `Dropout` layers to prevent overfitting. Test if these changes improve test accuracy.

## Wrapping Up

Congratulations on building a complete deep learning project! This journey from CNN theory to a functional model for medical image classification is a significant achievement. Your skills are now part of the foundation for AI innovation.

We value your feedback to improve future programs. Please fill out the feedback section in the submission form to share what you enjoyed, found challenging, or suggest improvements.

Thank you for your hard work, and we look forward to your submissions!
