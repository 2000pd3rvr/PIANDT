# Patentability Analysis for Research Manuscripts

## Overview

**Patentable subject matter** typically includes:
- ✅ Novel processes/methods with specific technical implementations
- ✅ Systems/apparatus with concrete architectures
- ✅ Algorithms implemented in hardware/software systems
- ✅ Specific technical solutions to technical problems
- ✅ Practical applications with novel implementations

**NOT typically patentable**:
- ❌ Pure mathematical formulas/theorems (abstract ideas)
- ❌ Natural phenomena or laws of nature
- ❌ General frameworks/theories without specific implementation
- ❌ Abstract ideas without technical application

---

## Patentability Assessment by Paper

### ✅ **HIGHLY PATENTABLE**

#### **Paper #3: Spatiotemporal Fusion** ⭐⭐⭐
**Patent Potential: VERY HIGH**

**Patentable Aspects:**
1. **Hybrid SPAD-RGB Sensing Architecture**
   - Specific system architecture combining SPAD dToF sensors with RGB cameras
   - Novel dual-model detection framework (spatial + material detection modules)
   - Specific integration methodology for fusing temporal and spatial signals
   - **Patent Type**: System/Apparatus Patent

2. **Dual Detection Method**
   - Specific process for combining object detection with material classification
   - Novel fusion algorithm for spatiotemporal feature integration
   - Real-time processing pipeline (8ms inference)
   - **Patent Type**: Method/Process Patent

**Key Claims:**
- "A system for spatiotemporal object detection comprising: a SPAD time-of-flight sensor configured to capture temporal signals; an active pixel sensor configured to capture spatial RGB images; a dual-model architecture comprising a spatial detection module and a material detection module..."
- "A method for fusing temporal and spatial signals for enhanced object detection..."

**Note**: The thesis explicitly mentions this as warranting IP protection (line 4329).

---

#### **Paper #4: Food Safety (Milk Purity Detection)** ⭐⭐⭐
**Patent Potential: VERY HIGH**

**Patentable Aspects:**
1. **Non-Invasive Milk Purity Detection System**
   - Specific SPAD-based system for liquid purity assessment
   - Novel application of time-of-flight sensing to food safety
   - Specific preprocessing algorithms (ambient noise estimation, Poisson noise mitigation)
   - **Patent Type**: System/Method Patent

2. **Invisible Contamination Detection Method**
   - Novel method for detecting invisible contaminants (e.g., hydrogen peroxide) using temporal signals
   - Specific signal processing pipeline for purity classification
   - Multi-zone transient processing methodology
   - **Patent Type**: Method Patent

**Key Claims:**
- "A non-invasive method for detecting impurities in liquid food products using single-photon time-of-flight sensors..."
- "A system for milk purity assessment comprising: a SPAD sensor configured to capture transient signals from homogenised milk samples; a preprocessing module for noise estimation and subtraction; a classification module..."

**Commercial Value**: High - direct application to food safety industry

---

#### **Paper #2: Material Detection** ⭐⭐
**Patent Potential: HIGH**

**Patentable Aspects:**
1. **Long-Range Material Classification Method**
   - Specific signal processing method for extended-range material detection (up to 4m)
   - Multi-pixel transient stacking algorithm
   - Depth-integrated single-pixel transient processing method
   - **Patent Type**: Method Patent

2. **Multi-Zone Signal Processing System**
   - Specific architecture for processing 4×4 zone SPAD arrays
   - Novel stacking methodology for transient histograms
   - **Patent Type**: System Patent

**Key Claims:**
- "A method for long-range material classification from flat surfaces using time-resolved SPAD signals..."
- "A multi-zone transient processing system for material detection..."

---

#### **Paper #7: System/Application (Web Framework)** ⭐⭐
**Patent Potential: HIGH**

**Patentable Aspects:**
1. **Web-Based Material Detection Framework**
   - Specific system architecture for web-based SPAD sensor integration
   - Custom data format (.sto extension) for spatiotemporal feature storage
   - Real-time inference pipeline via web interface
   - **Patent Type**: System/Software Patent

**Key Claims:**
- "A web-based framework for real-time material detection using SPAD sensors..."
- "A system for browser-accessible material classification..."

---

### ⚠️ **POTENTIALLY PATENTABLE** (with specific implementation details)

#### **Paper #6: Methodology (Per-Bin Gaussian Mixture)** ⭐
**Patent Potential: MODERATE**

**Patentable Aspects:**
1. **Per-Bin Signal Processing Method**
   - Specific implementation of per-bin Gaussian mixture modeling
   - Novel discretization approach for temporal signal processing
   - **Patent Type**: Method Patent (if novel implementation details)

**Considerations:**
- Must demonstrate novel technical implementation beyond mathematical formula
- Focus on specific hardware/software implementation details
- Emphasize technical advantages (computational efficiency, accuracy improvements)

---

### ❌ **NOT PATENTABLE** (Theoretical/Analytical)

#### **Paper #1: PAWD Framework** ❌
**Patent Potential: LOW**

**Reason:**
- Theoretical framework/classification system
- Abstract organizational structure
- No specific technical implementation
- **Alternative**: Consider copyright protection for framework documentation

**Note**: While the framework itself isn't patentable, specific implementations guided by the framework (Papers #2, #3, #4) ARE patentable.

---

#### **Paper #5: Complexity Analysis** ❌
**Patent Potential: VERY LOW**

**Reason:**
- Pure theoretical analysis
- Mathematical complexity analysis
- No novel technical implementation
- **Alternative**: Academic publication only

---

## Recommended Patent Strategy

### **Priority 1: File Immediately** (Before Publication)

1. **Paper #3: Spatiotemporal Fusion System**
   - **Patent Type**: Utility Patent (System + Method)
   - **Timeline**: File before CVPR/ICCV submission
   - **Value**: Very High - core innovation

2. **Paper #4: Food Safety Detection System**
   - **Patent Type**: Utility Patent (Method + System)
   - **Timeline**: File before Nature Food/Food Chemistry submission
   - **Value**: High - direct commercial application

### **Priority 2: File Soon** (Within 6 months)

3. **Paper #2: Long-Range Material Detection**
   - **Patent Type**: Method Patent
   - **Value**: High - practical application

4. **Paper #7: Web Framework**
   - **Patent Type**: Software/System Patent
   - **Value**: Moderate - deployment architecture

### **Priority 3: Evaluate After Publication**

5. **Paper #6: Per-Bin Methodology**
   - **Patent Type**: Method Patent (if novel implementation)
   - **Value**: Moderate - depends on specific technical details

---

## Important Considerations

### ⚠️ **Publication vs. Patent Timeline**

**CRITICAL**: In most jurisdictions (US, EU, UK), you have:
- **12 months** from first public disclosure to file a patent application
- **Public disclosure includes**: Conference papers, journal publications, thesis defense, online posting

**Recommendation:**
1. **File provisional patents** for Papers #3 and #4 BEFORE publication
2. Provisional patents are cheaper ($70-300) and give you 12 months to file full patent
3. This protects your IP while allowing publication

### 📋 **What to Include in Patent Applications**

1. **Detailed technical implementation**
   - Specific algorithms and processing steps
   - Hardware configurations and sensor specifications
   - Software architecture and data flow
   - Performance metrics and advantages

2. **Novel technical features**
   - What makes your approach different from prior art
   - Technical advantages (speed, accuracy, cost)
   - Specific technical solutions to technical problems

3. **Practical applications**
   - Real-world use cases
   - Commercial viability
   - Industry applications

### 💰 **Cost Estimates**

- **Provisional Patent (US)**: $70-300 (filing fee)
- **Full Utility Patent (US)**: $5,000-15,000 (including attorney fees)
- **PCT International Application**: $3,000-5,000 additional
- **UK/European Patents**: Similar costs

### 🤝 **University IP Considerations**

**IMPORTANT**: If this research was conducted at a university:
- University may have **ownership rights** to inventions
- Check your employment/student agreement
- May need to file through university's technology transfer office
- University may cover patent costs in exchange for licensing rights

---

## Summary Table

| Paper | Patentability | Priority | Patent Type | Commercial Value |
|-------|--------------|----------|-------------|------------------|
| #3: Spatiotemporal Fusion | ⭐⭐⭐ Very High | **P1 - File Now** | System + Method | Very High |
| #4: Food Safety | ⭐⭐⭐ Very High | **P1 - File Now** | Method + System | Very High |
| #2: Material Detection | ⭐⭐ High | P2 - File Soon | Method | High |
| #7: Web Framework | ⭐⭐ High | P2 - File Soon | Software/System | Moderate |
| #6: Methodology | ⭐ Moderate | P3 - Evaluate | Method (if novel) | Moderate |
| #1: PAWD Framework | ❌ Low | Not Patentable | N/A | N/A |
| #5: Complexity Analysis | ❌ Very Low | Not Patentable | N/A | N/A |

---

## Next Steps

1. **Immediately**: Consult with patent attorney or university tech transfer office
2. **Before Publication**: File provisional patents for Papers #3 and #4
3. **Document**: Maintain detailed lab notebooks and implementation records
4. **Prior Art Search**: Conduct patent search to ensure novelty
5. **Timeline**: Coordinate patent filing with publication timeline

---

## Contact Information for Patent Services

- **University Tech Transfer Office**: Check with University of Edinburgh
- **UK Intellectual Property Office**: https://www.gov.uk/government/organisations/intellectual-property-office
- **USPTO**: https://www.uspto.gov/
- **European Patent Office**: https://www.epo.org/

---

**Disclaimer**: This analysis is for informational purposes only and does not constitute legal advice. Consult with a qualified patent attorney before filing any patent applications.

