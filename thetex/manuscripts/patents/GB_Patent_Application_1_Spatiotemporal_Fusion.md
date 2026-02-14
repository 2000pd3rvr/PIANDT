# UK PATENT APPLICATION
## GB Patent Application No: [To be assigned by UKIPO]

---

**TITLE:**
A System and Method for Spatiotemporal Object Detection Using Hybrid Single-Photon Time-of-Flight and Active Pixel Sensors

---

**APPLICANT:**
A. Akuoko, D. Chitnis, and I. Gyongy
[Address to be provided]

---

**INVENTOR:**
A. Akuoko, D. Chitnis, and I. Gyongy

---

**PRIORITY DATE:**
[Date of filing]

---

## ABSTRACT

A system and method for enhanced object detection and material classification through the fusion of spatially resolved intensity images and time-resolved transient signals. The system comprises a single-photon avalanche diode (SPAD) time-of-flight sensor configured to capture one-dimensional temporal photon arrival histograms, an active pixel sensor (APS) configured to capture two-dimensional spatially resolved RGB intensity images, and a dual-model processing architecture. The spatial detection module processes RGB images for object localisation and classification, while the material detection module processes transient signals for material composition classification. The system achieves combined detection performance of 94.5% to 98.5% accuracy with near-real-time processing speeds of approximately 8 milliseconds, enabling reliable material-aware scene understanding for safety-critical applications including autonomous vehicles and robotic manipulation.

---

## FIELD OF THE INVENTION

This invention relates to machine vision systems, and more particularly to systems and methods for combining spatial and temporal signal processing for enhanced object detection with material awareness.

---

## BACKGROUND OF THE INVENTION

Contemporary machine vision systems rely predominantly on two-dimensional spatially resolved images for object detection and scene understanding. However, such systems face fundamental limitations in extracting structural features such as material composition, true depth, and subsurface scattering characteristics that are more accurately inferred from time-resolved signals.

Existing approaches to three-dimensional perception typically employ stereoscopic methods or indirect time-of-flight (iToF) sensors that estimate depth through phase-shift analysis. These methods suffer from computational complexity, reduced accuracy under adverse conditions, and inability to distinguish between objects with identical appearance but different material compositions.

Single-photon avalanche diode (SPAD) direct time-of-flight (dToF) sensors capture temporal photon arrival distributions that encode material-specific optical properties through subsurface scattering and reflectivity profiles. However, prior art has not successfully integrated SPAD temporal signals with spatial RGB imagery in a unified detection framework that simultaneously provides object localisation and material classification.

There exists a need for a system that combines spatial and temporal sensing modalities to enable enhanced scene understanding with material awareness, addressing limitations of appearance-based detection systems while maintaining computational efficiency suitable for real-time applications.

---

## SUMMARY OF THE INVENTION

According to a first aspect of the present invention, there is provided a system for spatiotemporal object detection, the system comprising:

a) a single-photon avalanche diode (SPAD) time-of-flight sensor configured to:
   - emit pulsed illumination at a wavelength of approximately 940 nanometers;
   - capture time-resolved transient signals comprising one-dimensional photon arrival histograms;
   - output temporal data representing material-dependent optical properties;

b) an active pixel sensor (APS) configured to:
   - capture two-dimensional spatially resolved RGB intensity images;
   - output spatial data representing geometric and appearance features;

c) a dual-model processing architecture comprising:
   - a spatial detection module configured to process RGB images and output object bounding box coordinates, class labels, and confidence scores;
   - a material detection module configured to process transient signals and output material class probabilities;
   - a fusion module configured to combine outputs from both modules to provide unified object detection with material awareness.

The system is characterised in that the material detection module processes 16×16 pixel transient images derived from a 4×4 zone SPAD array, where each zone contributes a one-dimensional cropped transient histogram arranged into a pseudo-image representation, and wherein the material classifier achieves validation accuracy of approximately 99% with inference times of 1-5 milliseconds.

According to a second aspect of the present invention, there is provided a method for spatiotemporal object detection, the method comprising the steps of:

a) simultaneously capturing, from a common target scene:
   - time-resolved transient signals using a SPAD time-of-flight sensor;
   - spatially resolved RGB intensity images using an active pixel sensor;

b) processing the RGB images through a spatial detection module to generate:
   - object bounding box coordinates;
   - object class labels;
   - spatial confidence scores;

c) processing the transient signals through a material detection module to generate:
   - material class probabilities;
   - material confidence scores;

d) fusing the spatial and material detection outputs to provide unified object detection with material composition information.

The method is characterised in that the transient signals are processed using a per-bin Gaussian mixture model where the expected photon count per bin i is given by:

μ_i = Σ(m=1 to M) [S_m / √(2πσ_m²)] × exp(-(t_i - t_{0,m})² / (2σ_m²)) + b

where S_m is the total signal photons for material m, σ_m is the standard deviation, t_{0,m} is the peak time for material m, M is the number of materials, and b represents ambient noise per bin.

---

## DETAILED DESCRIPTION OF THE INVENTION

### System Architecture

The invention provides a hybrid sensing system that combines SPAD direct time-of-flight (dToF) sensors with active pixel sensors (APS) to enable simultaneous object detection and material classification. The system architecture comprises three primary components: sensing hardware, signal processing modules, and fusion logic.

### Sensing Hardware

**SPAD Time-of-Flight Sensor:**
The SPAD sensor employed in the preferred embodiment is a 4×4 zone array detector with integrated illumination source operating at approximately 940 nanometers wavelength. Each zone captures time-resolved photon arrival histograms with temporal resolution of approximately 250 picoseconds per bin, providing up to 144 time bins per histogram. The sensor operates in direct time-of-flight mode, measuring photon round-trip travel times to encode both target distance and material-dependent optical properties.

The SPAD sensor configuration includes:
- Monochromatic infrared illumination source (Class 1 laser, ~940 nm)
- 4×4 pixel array with per-pixel time-to-digital converters (TDC)
- Temporal resolution: 250 ps per bin
- Maximum range: up to 4 meters
- Field of view: approximately 30 degrees

**Active Pixel Sensor (APS):**
The APS captures two-dimensional spatially resolved RGB intensity images at standard resolutions (e.g., 224×224 pixels for processing). The sensor operates in conventional imaging mode, providing geometric and appearance information complementary to the temporal signals from the SPAD sensor.

### Signal Processing Architecture

**Spatial Detection Module:**
The spatial detection module processes RGB images using state-of-the-art object detection architectures. **It is important to emphasize that while the system was experimentally validated using YOLOv3, YOLOv8, and DINOv3 architectures, the invention is not limited to these specific models.** The spatial detection module is designed to be architecture-agnostic and can work with any spatial object detection system, including but not limited to:

- Deep learning-based models (YOLO variants, DINOv3, SSD, Faster R-CNN, RetinaNet, etc.)
- Physics-based models (geometric feature extraction, edge detection, template matching, etc.)
- Hybrid approaches combining machine learning with physical constraints
- Future spatial detection architectures that may be developed

The module outputs:
- Bounding box coordinates (x, y, width, height)
- Object class labels
- Confidence scores

In the preferred embodiment, experimental validation was performed using YOLOv3, YOLOv8, and DINOv3. YOLOv8 achieved object detection accuracy of approximately 98% with inference times of 68 milliseconds for 224×224 pixel inputs on CPU hardware. However, the system's fusion architecture is designed to accept outputs from any spatial detection system that provides bounding box coordinates, class labels, and confidence scores, making it compatible with physics-based models, traditional computer vision algorithms, and future deep learning architectures.

**Material Detection Module:**
The material detection module processes transient signals using a custom convolutional neural network architecture. The input format is a 16×16 pixel pseudo-image derived from stacking 16 one-dimensional transient histograms from the 4×4 SPAD array zones.

The material classifier architecture comprises:
- Input: 16×16×3 tensor (three stacked transient-derived modalities per zone)
- Convolutional layers: progressive feature channels (1, 3, 32, 64, 128)
- Global average pooling for dimensionality reduction
- Fully connected layers with dropout regularization (rates: 0.5, 0.3)
- Output: Material class logits

The material classifier achieves validation accuracy of approximately 99% with inference times of 1-5 milliseconds, operating on CPU hardware.

**Signal Processing Models:**
Temporal signals are modeled using per-bin Gaussian mixture approximations. For multi-material surfaces, the expected photon count per bin i is:

μ_i = Σ(m=1 to M) [S_m / √(2πσ_m²)] × exp(-(t_i - t_{0,m})² / (2σ_m²)) + b

where:
- S_m: total signal photons for material m across the entire peak
- σ_m: standard deviation of Gaussian profile for material m
- t_{0,m}: peak arrival time for material m
- M: number of composite materials
- b: ambient noise photons per bin
- t_i: temporal position of bin i

This model accounts for the superposition of multiple material responses, where each constituent material contributes a distinct temporal signature characterized by signal strength, temporal spread, and peak arrival time.

### Fusion Methodology

The fusion module combines outputs from spatial and material detection modules to provide unified object detection with material awareness. The combined performance is calculated as a weighted average of spatial detection accuracy and material classification accuracy, with equal weighting in the preferred embodiment.

The system achieves combined dual detection performance of:
- YOLOv3 + Material Classifier: 94.5% accuracy
- YOLOv8 + Material Classifier: 98.5% accuracy at ~8 ms processing time
- DINOv3 + Material Classifier: 95.5% accuracy

### Preprocessing

Transient signals undergo preprocessing to mitigate noise and ambiguities:
1. **Ambient noise estimation**: Baseline estimated from initial histogram bins where target signals do not accumulate
2. **Poisson noise mitigation**: Mean value estimation and subtraction across all time bins
3. **Peak extraction**: Signal peaks extracted at full-width at half-maximum (FWHM), typically spanning 8 bins with 4-bin padding on each side

### Advantages

The invention provides several technical advantages:
1. **Material awareness**: Enables distinction between objects with identical appearance but different material compositions
2. **Robustness**: Reduces susceptibility to adversarial examples and spoofing attacks
3. **Real-time performance**: Achieves near-real-time processing (8 ms) suitable for safety-critical applications
4. **Low computational overhead**: Material classification requires minimal processing (1-5 ms)
5. **Complementary information**: Spatial features provide localisation while temporal features encode structural properties

---

## CLAIMS

**Claim 1:** A system for spatiotemporal object detection, the system comprising:
- a single-photon avalanche diode (SPAD) time-of-flight sensor configured to capture time-resolved transient signals comprising one-dimensional photon arrival histograms;
- an active pixel sensor (APS) configured to capture two-dimensional spatially resolved RGB intensity images;
- a spatial detection module configured to process said RGB images and output object bounding box coordinates, class labels, and confidence scores;
- a material detection module configured to process said transient signals and output material class probabilities;
- a fusion module configured to combine outputs from said spatial detection module and said material detection module to provide unified object detection with material awareness.

**Claim 2:** The system of Claim 1, wherein the SPAD sensor comprises a 4×4 zone array detector with integrated illumination source operating at approximately 940 nanometers wavelength.

**Claim 3:** The system of Claim 1, wherein the material detection module processes 16×16 pixel transient images derived from stacking 16 one-dimensional transient histograms from the 4×4 SPAD array zones.

**Claim 4:** The system of Claim 1, wherein the material detection module employs a convolutional neural network architecture with progressive feature channels (1, 3, 32, 64, 128) and global average pooling.

**Claim 5:** The system of Claim 1, wherein the transient signals are processed using a per-bin Gaussian mixture model where the expected photon count per bin i is given by:

μ_i = Σ(m=1 to M) [S_m / √(2πσ_m²)] × exp(-(t_i - t_{0,m})² / (2σ_m²)) + b

**Claim 6:** The system of Claim 1, wherein the material detection module achieves validation accuracy of at least 99% with inference times of 1-5 milliseconds.

**Claim 7:** The system of Claim 1, wherein the combined dual detection system achieves accuracy of at least 94.5% with processing times of approximately 8 milliseconds.

**Claim 8:** A method for spatiotemporal object detection, the method comprising:
- simultaneously capturing time-resolved transient signals using a SPAD time-of-flight sensor and spatially resolved RGB intensity images using an active pixel sensor;
- processing said RGB images through a spatial detection module to generate object bounding box coordinates, class labels, and confidence scores;
- processing said transient signals through a material detection module to generate material class probabilities;
- fusing outputs from said spatial and material detection modules to provide unified object detection with material composition information.

**Claim 9:** The method of Claim 8, wherein the transient signals are preprocessed by estimating ambient noise from initial histogram bins and subtracting Poisson noise through mean value estimation.

**Claim 10:** The method of Claim 8, wherein signal peaks are extracted at full-width at half-maximum (FWHM) spanning 8 bins with 4-bin padding on each side.

**Claim 11:** The system or method of any preceding claim, wherein the spatial detection module is architecture-agnostic and can employ any spatial object detection system including, but not limited to, YOLOv3, YOLOv8, DINOv3, other deep learning models, physics-based models, or hybrid approaches, provided that the system outputs bounding box coordinates, class labels, and confidence scores.

**Claim 12:** The system or method of any preceding claim, configured for use in autonomous vehicles, robotic manipulation, or security surveillance applications.

---

## DRAWINGS

**Figure 1:** System architecture diagram showing the processing pipeline from observed scene through measured signal to the PAWD framework, illustrating how spatial and structural features combine to form spatiotemporal decisions. The diagram demonstrates the modular design where the spatial detection module can accept inputs from any spatial object detection system (including but not limited to YOLO variants, DINOv3, physics-based models, or other spatial detection architectures), while the material detection module processes transient signals. The fusion module combines outputs from both modules to provide unified object detection with material awareness.

[FIGURE_1_1_TIKZ]

**Figure 2:** Signal processing flow diagram illustrating temporal and spatial signal paths

**Figure 3:** Material detection module architecture (16×16×3 input, convolutional layers, classification head)

**Figure 4:** Example detection results showing object localisation with material classification

---

## DECLARATION

We, A. Akuoko, D. Chitnis, and I. Gyongy, declare that:
1. We are the inventors of the invention described in this application;
2. The invention has not been publicly disclosed prior to the filing date of this application;
3. To the best of our knowledge, the invention is novel and involves an inventive step;
4. We are entitled to apply for a patent for this invention.

**Signature:** _________________________

**Date:** _________________________

---

**END OF SPECIFICATION**

