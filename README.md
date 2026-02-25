# Breaking Isolation: A New Perspective on Hypervisor Exploitation via Cross-Domain Attacks

This repository contains artefacts for our research paper 
"Breaking Isolation: A New Perspective on Hypervisor Exploitation via Cross-Domain Attacks".

Cross-Domain Attacks (CDA) introduce a new exploitation paradigm for hypervisors by systematically leveraging guest memory as a reusable exploitation substrate. We demonstrate that the memory-mapping design of modern hypervisors unintentionally exposes powerful cross-domain primitives. By redirecting corrupted host pointers into attacker-controlled guest memory, CDA transforms previously hard-to-exploit pointer corruption bugs into practical and reliable exploitation paths.



|                  |                                                              |
| ---------------- | ------------------------------------------------------------ |
| **Authors**      | Gaoning Pan, Yiming Tao, Qinying Wang, Chunming Wu, Mingde Hu, Yizhi Ren, Shouling Ji |
| **Organization** | Hangzhou Dianzi University; Zhejiang University; EPFL        |
| **Published at** | Network and Distributed System Security Symposium (NDSS 2026) |
| **Paper**        | https://www.arxiv.org/pdf/2512.04260                         |

# Overview

Our artefacts are structured as follows:


- **Gadget Identification**:  
  CodeQL-based static analysis for discovering cross-domain gadgets, as described in §5 of our paper.

- **Gadget Triggering (Fuzzing)**:  
  Fuzzing pipeline for generating inputs that trigger identified cross-domain gadgets.

- **PoC Reconstruction**:  
  GDB-assisted extraction and reconstruction of standalone executable PoCs from fuzz-generated seed files.
