# UK PATENT APPLICATION
## GB Patent Application No: [To be assigned by UKIPO]

---

**TITLE:**
A Non-Invasive System and Method for Liquid Food Purity Detection Using Single-Photon Time-of-Flight Sensing

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

A non-invasive system and method for detecting impurities in liquid food products, particularly homogenised milk, using single-photon avalanche diode (SPAD) time-of-flight sensors. The system captures time-resolved transient signals that encode material-dependent optical properties through subsurface scattering and reflectivity profiles. A convolutional neural network classifier processes multi-zone transient images to distinguish pure consumable states from contaminated or degraded states, including invisible contaminants that produce no discernible visual changes. The system achieves approximately 98% training accuracy and 93.33% validation accuracy for binary purity classification, with the ability to detect invisible contamination at approximately 96% accuracy. The method is non-invasive, requiring no sample extraction or container opening, and operates with processing times of 1-5 milliseconds, making it suitable for both domestic and commercial food safety applications.

---

## FIELD OF THE INVENTION

This invention relates to food safety assessment systems, and more particularly to non-invasive methods for detecting impurities in liquid food products using optical time-of-flight sensing.

---

## BACKGROUND OF THE INVENTION

Food purity assessment is critical for ensuring consumer safety and product quality. Traditional methods for detecting impurities in liquid foods, particularly milk, include chemical assays, near-infrared (NIR) spectroscopy, and visual inspection. However, these methods suffer from significant limitations:

Chemical assays are consumptive, requiring sample extraction and destruction of the product. They are also time-consuming and require specialized laboratory equipment and expertise.

NIR spectroscopy systems are expensive, operationally complex, and require specialist calibration. They typically cost tens of thousands of pounds and demand significant technical expertise for operation and maintenance.

Visual inspection and RGB imaging-based methods depend entirely on observable changes in color, consistency, or appearance. Many contaminants, such as hydrogen peroxide, produce no visible changes in the bulk sample, making them undetectable through conventional imaging approaches.

There exists a need for a low-cost, non-invasive, and reliable method for detecting both visible and invisible contaminants in liquid food products, particularly for applications where rapid assessment is required without compromising product integrity.

Single-photon avalanche diode (SPAD) time-of-flight sensors capture temporal photon arrival distributions that encode material-specific optical properties through subsurface scattering. However, prior art has not successfully applied SPAD sensing to liquid food purity assessment, particularly for detecting invisible contaminants in homogenised milk products.

---

## SUMMARY OF THE INVENTION

According to a first aspect of the present invention, there is provided a system for non-invasive liquid food purity detection, the system comprising:

a) a single-photon avalanche diode (SPAD) time-of-flight sensor configured to:
   - emit pulsed illumination at a wavelength of approximately 940 nanometers;
   - capture time-resolved transient signals from a liquid food sample;
   - output temporal data representing material-dependent optical properties;

b) a preprocessing module configured to:
   - estimate ambient noise from initial histogram bins where target signals do not accumulate;
   - mitigate Poisson noise through mean value estimation and subtraction;
   - extract signal peaks at full-width at half-maximum (FWHM);

c) a material classification module configured to:
   - process multi-zone transient images derived from a 4×4 SPAD array;
   - classify samples as pure or impure based on temporal scattering signatures;
   - output binary purity assessment with confidence scores.

The system is characterised in that it detects invisible contaminants that produce no discernible visual changes in the bulk sample, achieving detection accuracy of approximately 96% for invisible contamination including hydrogen peroxide and sugar impurities.

According to a second aspect of the present invention, there is provided a method for non-invasive liquid food purity detection, the method comprising the steps of:

a) positioning a SPAD time-of-flight sensor at a distance of 20-30 centimeters from a liquid food container;

b) capturing time-resolved transient signals comprising photon arrival histograms;

c) preprocessing said transient signals by:
   - estimating ambient noise baseline from initial histogram bins;
   - subtracting Poisson noise through mean value estimation;
   - extracting signal peaks spanning 8 bins with 4-bin padding;

d) processing preprocessed transient signals through a convolutional neural network classifier to generate binary purity classification (pure or impure);

e) outputting purity assessment with confidence scores.

The method is characterised in that it operates on homogenised liquid samples and distinguishes pure consumable states from contaminated or degraded states without requiring sample extraction or container opening.

---

## DETAILED DESCRIPTION OF THE INVENTION

### System Architecture

The invention provides a non-invasive purity detection system that exploits temporal photon transport characteristics encoded in SPAD time-of-flight measurements. The system architecture comprises sensing hardware, signal preprocessing modules, and a material classification network.

### Sensing Hardware

**SPAD Time-of-Flight Sensor:**
The SPAD sensor employed in the preferred embodiment is a 4×4 zone array detector with integrated illumination source operating at approximately 940 nanometers wavelength. The sensor is positioned 20-30 centimeters from the liquid food container surface, with a field of view of approximately 30 degrees.

Key sensor specifications:
- Monochromatic infrared illumination (Class 1 laser, ~940 nm)
- 4×4 pixel array with per-pixel time-to-digital converters
- Temporal resolution: 250 picoseconds per bin
- Maximum of 144 time bins per histogram
- Field of view: approximately 30 degrees

The 30-degree field of view ensures that:
- At 20 cm distance: coverage diameter of approximately 10.7 cm
- At 30 cm distance: coverage diameter of approximately 16.1 cm
- Sufficient coverage of standard 100 mL bottles (diameter 5-6 cm) and 1 L containers (width 7-9 cm)
- Exclusion of background targets through geometric isolation

### Signal Processing

**Preprocessing:**
Transient signals undergo preprocessing to mitigate noise and extract relevant features:

1. **Ambient Noise Estimation:**
   - Baseline estimated from initial histogram bins where target signals do not accumulate
   - Per-frame estimation to handle dynamic illumination conditions
   - Subtraction across all bins to improve signal-to-background ratio

2. **Poisson Noise Mitigation:**
   - Mean value estimation across all time bins
   - Subtraction to account for shot noise in photon counting

3. **Peak Extraction:**
   - Edge detection to identify sharp rises above defined threshold
   - Centre-of-mass (CoM) extraction to locate signal peak
   - Full-width at half-maximum (FWHM) extraction spanning 8 bins
   - 4-bin padding on left and right sides for signal augmentation

**Material Classification:**
The classification module employs a feedforward 2D convolutional neural network designed for binary purity assessment. The input format is a 16×16 pixel pseudo-image derived from stacking 16 one-dimensional transient histograms from the 4×4 SPAD array zones.

Network architecture:
- Input: 16×16×3 tensor (three stacked transient-derived modalities per zone)
- Convolutional layers: progressive feature channels (1, 3, 32, 64, 128)
- Global average pooling for dimensionality reduction
- Fully connected layers with dropout regularization (rates: 0.5, 0.3)
- Output: Binary classification (pure/impure) with confidence scores

### Contaminant Detection

**Material Contaminants:**
The system detects material impurities classified by matter states:
- Solid-phase contaminants (e.g., sugar, particulate matter)
- Liquid-phase contaminants (e.g., water, other liquids)
- Gaseous-phase contaminants (e.g., air, volatile compounds)

Detection range: 100-500 parts per million (ppm) for extreme sensitivity, with experimental validation up to 10,000 ppm (0.05%-1% impurity concentration).

**Non-Material Contaminants:**
The system detects non-material contamination arising from:
- Poor storage temperature conditions (resulting in clotting and suspension)
- Temporal degradation beyond best-before or expiry dates

**Invisible Contamination:**
A critical capability is detection of invisible contaminants that produce no discernible visual changes. The system achieves approximately 96% accuracy in detecting:
- Hydrogen peroxide contamination (liquid-phase impurity)
- Sugar contamination (solid-phase impurity)

These contaminants remain visually indistinguishable from pure controls under standard ambient lighting, yet produce detectable changes in temporal scattering signatures.

### Performance Characteristics

**Training Performance:**
- Binary purity classification: approximately 98% training accuracy
- Multi-label classification (all contaminant types): approximately 80% convergence

**Validation Performance:**
- Previously unseen samples: approximately 93.33% accuracy
- Invisible contamination detection: approximately 96% accuracy
- Out-of-distribution rejection: >80% confidence for invalid inputs (e.g., solid surfaces)

**Generalisation:**
The system demonstrates generalisation across:
- Multiple manufacturers (four commercial milk brands tested)
- Varying fat contents (0.3%, 1.8%, 3.7%, 14%)
- Different container types (transparent and translucent)
- Temporal variations in acquisition

**Processing Speed:**
- Inference time: 1-5 milliseconds per sample
- Suitable for real-time applications and high-throughput screening

### Advantages

The invention provides several technical advantages:

1. **Non-Invasive:** Requires no sample extraction or container opening
2. **Invisible Contamination Detection:** Detects contaminants that produce no visual changes
3. **Low Cost:** Utilizes compact, low-budget SPAD sensors compared to expensive NIR spectrometers
4. **Rapid Processing:** 1-5 millisecond inference times enable real-time assessment
5. **Generalisation:** Works across different manufacturers and fat contents
6. **Reliability:** High accuracy (98% training, 93.33% validation) with robust performance
7. **Practical Deployment:** Suitable for both domestic and commercial applications

### Applications

The system is applicable to:
- Consumer food safety testing (domestic use)
- Commercial quality control in dairy processing
- Retail point-of-sale purity verification
- Food safety inspection and compliance
- Research and development in food science

---

## CLAIMS

**Claim 1:** A system for non-invasive liquid food purity detection, the system comprising:
- a single-photon avalanche diode (SPAD) time-of-flight sensor configured to capture time-resolved transient signals from a liquid food sample;
- a preprocessing module configured to estimate ambient noise, mitigate Poisson noise, and extract signal peaks from said transient signals;
- a material classification module configured to process multi-zone transient images and classify samples as pure or impure based on temporal scattering signatures.

**Claim 2:** The system of Claim 1, wherein the SPAD sensor comprises a 4×4 zone array detector with integrated illumination source operating at approximately 940 nanometers wavelength, positioned 20-30 centimeters from the liquid food container.

**Claim 3:** The system of Claim 1, wherein the preprocessing module estimates ambient noise from initial histogram bins where target signals do not accumulate and subtracts said baseline across all bins.

**Claim 4:** The system of Claim 1, wherein the preprocessing module extracts signal peaks at full-width at half-maximum (FWHM) spanning 8 bins with 4-bin padding on each side.

**Claim 5:** The system of Claim 1, wherein the material classification module processes 16×16 pixel transient images derived from stacking 16 one-dimensional transient histograms from the 4×4 SPAD array zones.

**Claim 6:** The system of Claim 1, wherein the material classification module employs a convolutional neural network with progressive feature channels (1, 3, 32, 64, 128) and global average pooling.

**Claim 7:** The system of Claim 1, configured to detect invisible contaminants that produce no discernible visual changes in the bulk sample, achieving detection accuracy of at least 96%.

**Claim 8:** The system of Claim 1, wherein the liquid food product is homogenised milk, and the system achieves binary purity classification accuracy of at least 98% training accuracy and 93.33% validation accuracy.

**Claim 9:** A method for non-invasive liquid food purity detection, the method comprising:
- positioning a SPAD time-of-flight sensor at a distance of 20-30 centimeters from a liquid food container;
- capturing time-resolved transient signals comprising photon arrival histograms;
- preprocessing said transient signals by estimating ambient noise, mitigating Poisson noise, and extracting signal peaks;
- processing preprocessed transient signals through a convolutional neural network classifier to generate binary purity classification;
- outputting purity assessment with confidence scores.

**Claim 10:** The method of Claim 9, wherein the preprocessing step estimates ambient noise baseline from initial histogram bins and subtracts said baseline across all bins.

**Claim 11:** The method of Claim 9, wherein the preprocessing step extracts signal peaks at full-width at half-maximum (FWHM) spanning 8 bins with 4-bin padding.

**Claim 12:** The method of Claim 9, wherein the liquid food product is homogenised milk, and the method distinguishes pure consumable states from contaminated or degraded states.

**Claim 13:** The method of Claim 9, configured to detect invisible contaminants including hydrogen peroxide and sugar impurities that produce no discernible visual changes.

**Claim 14:** The system or method of any preceding claim, wherein the system operates with inference times of 1-5 milliseconds per sample.

**Claim 15:** The system or method of any preceding claim, configured for use in consumer food safety testing, commercial quality control, or retail point-of-sale verification.

---

## DRAWINGS

[To be included: System architecture diagram, signal processing flow, example purity assessment results]

**Figure 1:** System architecture showing SPAD sensor positioned relative to liquid food container

**Figure 2:** Signal processing flow diagram illustrating preprocessing and classification steps

**Figure 3:** Material classification module architecture (16×16×3 input, convolutional layers, binary classification head)

**Figure 4:** Example purity assessment results showing pure vs. contaminated sample discrimination

**Figure 5:** Principal component analysis visualization showing separation between pure and invisibly contaminated samples

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

