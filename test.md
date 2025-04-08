## How did you spend your time

### Mempool research

Since early 2022, I have been working on a mempool data collection and analysis project with Clara Shikhelman (Head of Research at Chaincode Labs), Paolo Guasoni (Professor of Financial Mathematics at Dublin University), and Gur Huberman (Professor of Behavioral Finance at Columbia University). The goal of this research is to formalize a statistical understanding of the mempool and provide a dataset for ongoing research into fee estimation, mempool congestion, and pinning and replacement behavior.

Not much has changed on this project since my last report. Since January I have:

* Working on a transaction level dataset for analysis
* Continuing to meet with the student team as they formalize a data pipeline
* Used the data for fee estimation research (in conjuction with Clara Shikhelman)

### Technical contributions

#### Silent payments (BIP-352)

I have been working on Silent Payments with Ruben Somsen since January 2023. Silent payments is a privacy and usability improvement for Bitcoin which allows users to have a static payment address, allowing them to receive multiple payments without on-chain address reuse.

Since January I have:

* Updated test vectors and responded to review on the BIP (co-authored with Ruben Somsen)
  * [BIP draft](https://github.com/bitcoin/bips/pull/1458)
  * At this point, we are considering the protocol finalized and waiting for the BIP to be merged
* Reviewed and helped with the design of a `libsecp256k1` silent payments module
  * [Module PR](https://github.com/bitcoin-core/secp256k1/pull/1471)
  * Re-wrote [#28122](https://github.com/bitcoin/bitcoin/pulls/28122) to use the new POC module
  * Designing the module is expected to be an ongoing effort
  * All Bitcoin Core related PRs can be tracked here: [Tracking issue](https://github.com/bitcoin/bitcoin/issues/28536)
* Helped with [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), a rust library for BIP352
  * https://github.com/cygnet3/rust-silentpayments/pull/66
  * https://github.com/cygnet3/rust-silentpayments/pull/72
* As part of working with `rust-silentpayments`, upstreamed changes to [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin)
  * https://github.com/rust-bitcoin/rust-bitcoin/pull/2451
  * https://github.com/rust-bitcoin/rust-bitcoin/pull/2356

#### Warnet

In May 2023, I proposed a simulation and stress testing framework for Bitcoin with the goal of stress testing and analyzing p2p emergent behaviors. I joined a small hackathon team in August to build out a proof of concept, and development has been ongoing since with a goal of us having our first official release of the software in January 2024.

Since January I have:

* Continued to work towards getting the software release ready, specifically focusing on review and K8s support
  * Helping mostly as a reviewer: [PRs opened or reviewed by me](https://github.com/search?q=org%3Abitcoin-dev-project+is%3Apr+involves%3A%40me&type=pullrequests)
* Project: https://github.com/bitcoin-dev-project/warnet

#### Ongoing contributions and review to Bitcoin Core

As part of my ongoing contributions to Bitcoin Core, since January I have:

* Helped with the v27/backports releases of Bitcoin Core, as a tester and guix builder
  * [v27.0rc1](https://github.com/bitcoin-core/guix.sigs/pull/1056)
  * [v26 backport](https://github.com/bitcoin-core/guix.sigs/pull/1023)
* Been involved in [ongoing review](https://github.com/search?q=repo%3Abitcoin%2Fbitcoin+is%3Apr+involves%3A%40me&type=pullrequests)
* Helped "Legacy wallet removal" meet the v27 timeline by reviewing:
  * https://github.com/bitcoin/bitcoin/pull/29403
  * https://github.com/bitcoin/bitcoin/pull/28987
  * https://github.com/bitcoin/bitcoin/pull/26008
  * https://github.com/bitcoin/bitcoin/pull/29112

### Community

In addition to my technical contributions, I co-organize the Bitcoin Amsterdam Bitdevs, with our most recent meeting attended by over 50 people. In addition to BitDevs, I have been mentoring several developers, setting aside a few hours every week for mentorship related to getting involved as a new contributor, answering technical questions, general advice, and accountability. 

Since January of 2024, I have:

* Mentoring one of the Qala Alumni and current BTrust Grantees
* Helping mentor the [BTCFoss Career](https://learning.chaincode.com/) program from Chaincode
  * Running weekly office hours and assisting students with questions


## How did you make use of the money?

Primarily, living expenses. In addition to normal living expenses, working on Bitcoin Core typically involves lots of travel for conferences and CoreDev meetups. In some cases, even organizers will help subsidize some travel expenses, but typically airfare and lodging are paid out of pocket.

## What do you plan to work on next quarter

My primary focus for next guarter will be:

* Silent Payments. The project plan is listed here: https://github.com/bitcoin/bitcoin/issues/28536
  * Since January, I've shifted priorities in favor of working on the libsecp256k1 module as this is a prerequisite for silent payments being included in Bitcoin Core
  * The Bitcoin Core PRs are still open, but won't be merged until the libsecp256k1 module is finalized
* Continued work on Warnet
* On-going review and contributions in Bitcoin Core
