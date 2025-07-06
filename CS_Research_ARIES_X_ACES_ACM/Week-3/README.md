# **WEEK 3**

## Pixels to Patterns

## By: ACES ACM x ARIES

# **Focus Areas**

* Understand CNNs  
* Explore Architectures  
* Hands-on Training


# **Part 1: Inside a CNN**

### *Objective:*

To understand how Convolutional Neural Networks (CNNs) process image data by breaking it down into features using layers like convolution, pooling, and activation , and build intuition for how models “see” and learn patterns.

### *Expectations:*

* Grasp how convolutional filters work on images  
* Know the role of pooling and activations  
* Visualize how CNNs extract features layer by layer

### *Resources:*

* [Convolutional Neural Networks](https://youtu.be/oGpzWAlP5p0?si=yBxFM5KLf_-eowov)

   | Understand the basics of CNNs : how convolution and filters work to detect patterns in images, building from edges to complex features. |
   | :---- |

* [CNN Visualized](https://youtu.be/pj9-rr1wDhM?si=oIslnz23QPKawUDD)

   | Visualize the internal operations of a CNN: convolution, activation, pooling, and see how images get transformed layer by layer. |
   | :---- |

# **Part 2: Building Deeper Nets**

### *Objective:*

To understand the design and working principles of AlexNet and ResNet architectures through reading and video demonstrations of implementations.

### *Expectations:*

* Get familiar with the structure and layers of AlexNet  
* Understand the concept of skip connections in ResNet  
* Watch and follow PyTorch and TensorFlow implementation walkthroughs  
* Prepare for hands-on training in upcoming parts


### *Resources:*

* [AlexNet PDF](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)

   | To study the original AlexNet architecture, layer details, and innovations that made it a breakthrough in image classification. |
   | :---- |


* [TensorFlow Implementation of AlexNet](https://youtu.be/c2kKFSkAF10?si=Mp8dRo7WnqeQ7pqs) 

   | To follow a practical AlexNet implementation in TensorFlow and understand coding details for building CNNs. |
   | :---- |


* [TensorFlow Implementation of ResNet](https://youtu.be/cwWFKL0wzi4?si=JE4cwwYAKjzO_kIz)  (OPTIONAL)

   | To see how ResNet is implemented inTenserflow, focusing on skip connections and overall architecture. |
   | :---- |


* [Pytorch Implementation of ResNet](https://youtu.be/DkNIBBBvcPs?si=3-JvPRbsxiO2rITy) (OPTIONAL)

   | To see how ResNet is implemented in PyTorch, focusing on skip connections and overall architecture. |
   | :---- |


# **Weekly Assignment**

### *What You Need To Do:*

1. **Pick a model:**  
   * Either AlexNet or ResNet (ResNet is optional if you want to try something more advanced)

2. **Prepare data:**  
   * Use Fashion-MNIST dataset (28x28 grayscale images, 10 classes)  
   * The images are already preprocessed (normalized and resized), so minimal processing is needed here  
   * *Note:* In real-world cases, images usually require more preprocessing steps like resizing, normalization, augmentation, and noise removal to improve results  
   * Split data into training, validation, and test sets

3. **Build and train:**  
   * Implement the chosen model architecture in your preferred framework (PyTorch/TensorFlow)  
   * Use suitable optimizer and loss function   
   * Train for enough epochs to get stable results

4. **Evaluate:**  
   * Calculate and report final test accuracy  
   * Plot training and validation accuracy/loss curves

5. **Write observations:**  
   * What worked well? Any training challenges?  
   * How did the model perform on different classes?  
   * Differences you noticed if you tried both models (optional)

### *Guidelines and Submission:*

* Code should be clean, modular, and well-commented  
* Save your trained model weights  
* Submit a **ZIP file** containing your code and report  
* **File name format:** `name_csresearch_w3.zip` (replace “name” with your actual name)  
* Report should include:  
  * Model chosen and brief architecture summary  
  * Final accuracy and training curves (accuracy and loss)  
  * Key observations and challenges

