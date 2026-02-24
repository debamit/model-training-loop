# Research Topics for Agent Economy System

## Critical Path Research (Must solve before building)

### 1. Reputation System Design
**Problem**: Prevent gaming while enabling cold start

**Research Questions**:
- How do existing web3 reputation systems handle Sybil attacks? (Gitcoin Passport, Worldcoin, Lens Protocol)
- What's the optimal reputation decay function? (time-based vs. activity-based)
- How to prevent wash trading to boost scores?
- Cold start solutions: bonding curves, vouching systems, or graduated limits?

**References to Study**:
- EigenTrust algorithm (P2P reputation)
- PageRank (reputation via network effects)
- Prediction market reputation (Augur, Polymarket)
- eBay/Airbnb reputation systems (centralized but proven UX)

---

### 2. Risk Pricing for Insurance Pools
**Problem**: Algorithmically price agent risk without historical data

**Research Questions**:
- How do AMMs handle impermanent loss? (can this model map to fraud risk?)
- What risk factors are most predictive? (stake size, transaction volume, age, dispute ratio)
- How to prevent adverse selection? (only risky agents buying coverage)
- Pool utilization ratio: what % of pool should be deployable vs. reserved?

**References to Study**:
- Nexus Mutual (on-chain insurance, how they price smart contract risk)
- Aave/Compound risk parameters (collateralization ratios, liquidation mechanics)
- Traditional actuarial models (pricing frameworks, not necessarily implementation)
- Uniswap V3 concentrated liquidity (capital efficiency)

---

### 3. Multi-LLM Arbitration Reliability
**Problem**: Ensure arbitration models can't be fooled

**Research Questions**:
- How aligned are different LLMs on prompt injection detection? (test GPT vs Claude vs Gemini)
- What's the adversarial success rate? (can you craft prompts that fool majority?)
- Cost per arbitration? (5 models x 10K token context = $?)
- What happens with model updates? (GPT-4 → GPT-5, does this change outcomes?)

**Experiments Needed**:
- Build dataset of prompt injections (Anthropic, OpenAI have some public datasets)
- Test inter-model agreement on 100 examples
- Red team: try to fool the ensemble
- Cost analysis: real-world conversation lengths × model pricing

**References to Study**:
- Anthropic's Constitutional AI (multi-model alignment)
- LLM jailbreak research (how attacks work)
- Ensemble learning (when does diversity help vs. hurt)

---

### 4. EigenLayer Integration & Slashing Mechanics
**Problem**: Actual implementation of restaking and slashing

**Research Questions**:
- How does EigenLayer AVS work in practice? (docs vs. reality)
- What's the slashing flow? (who triggers, how fast, appeals process?)
- Can we use existing AVS or need custom?
- What's the actual finality time for slashing decisions?

**Action Items**:
- Read EigenLayer whitepaper + docs thoroughly
- Join EigenLayer Discord/forums (ask questions)
- Check if anyone's built similar use case (agent economy AVS)
- Test on testnet: stake → slash → recover flow

**References to Study**:
- EigenLayer documentation
- Existing AVS implementations (oracle networks, bridges)
- Ethereum slashing spec (beacon chain validator slashing for comparison)

---

### 5. ERC-8004 Agent Standard
**Problem**: This might not exist yet? Need to define or adapt existing standard

**Research Questions**:
- Is ERC-8004 a real standard or hypothetical? (check EIPs.ethereum.org)
- If not real: what existing standards are closest? (ERC-725, ERC-1056 for identity?)
- What metadata must be in registry? (agent capabilities, stake, reputation, endpoint)
- How to handle agent updates/versioning?

**Action Items**:
- Search for existing agent/identity standards on Ethereum
- Look at ERC-725 (proxy identity), ERC-1056 (lightweight identity)
- Check what AI agent frameworks exist (AutoGPT, LangChain agents - how do they describe capabilities?)
- Draft a minimal schema for agent registry

---

### 6. Cross-Chain vs. Single L2 Strategy
**Problem**: Where does this system live?

**Research Questions**:
- Single L2 (which one? Base, Arbitrum, Optimism, custom?)
- Multi-chain from start (increases complexity 10x)
- How to handle agents needing to interact with multiple chains? (bridges, intents?)

**Decision Factors**:
- Cost (gas fees per transaction)
- Speed (confirmation times)
- Ecosystem (existing users, tools, liquidity)
- Sovereignty (own L2 = more control but more overhead)

**Action Items**:
- Compare L2 gas costs for typical transaction
- Check L2 finality times (soft vs. hard finality)
- Research rollup-as-a-service (Conduit, Caldera, AltLayer)

---

### 7. Oracle Requirements
**Problem**: What off-chain data do agents need?

**Research Questions**:
- Do agents need price feeds? (if transacting in USD terms)
- Do they need external API data? (weather, flight prices, etc.)
- How to verify data integrity in disputes?

**Options**:
- Chainlink (expensive but reliable)
- UMA (optimistic oracle, good for subjective data)
- API3 (first-party oracles)
- Agents self-report with slashing if wrong (optimistic approach)

---

### 8. Key Management for Agents
**Problem**: Agents need private keys, users need recovery

**Research Questions**:
- MPC wallets? (threshold signatures, no single point of failure)
- Account abstraction? (ERC-4337 for social recovery)
- Hardware enclaves? (TEE for key storage)
- How do users recover if they lose access to their agent?

**References to Study**:
- ERC-4337 (account abstraction)
- Safe (Gnosis Safe multisig patterns)
- Web3Auth, Magic (embedded wallet solutions)
- MPC wallet providers (Fireblocks, Qredo)

---

### 9. Privacy: Encryption for Conversations
**Problem**: Keep conversations private until dispute

**Research Questions**:
- Encrypt to who? (user + service agent + escrow key?)
- Where stored? (IPFS, Arweave, centralized DB?)
- How to ensure reveal works? (time-lock encryption, threshold decryption?)

**Options**:
- Lit Protocol (programmable encryption, threshold decryption)
- NuCypher (proxy re-encryption)
- Simple symmetric encryption with multi-party key shares
- Just hash conversations, store off-chain, reveal hash matches

---

### 10. Economic Modeling & Simulations
**Problem**: Will the incentives actually work?

**Research Questions**:
- Agent-based modeling: simulate agents gaming the system
- What attack vectors are most profitable?
- What parameter ranges (stake minimums, slashing %, pool fees) are stable?
- Under what conditions does the insurance pool go insolvent?

**Tools**:
- cadCAD (complex systems modeling)
- Python simulations (Monte Carlo for different scenarios)
- Game theory analysis (Nash equilibria, mechanism design)

**Scenarios to Model**:
- 1000 agents, 1% malicious, 10% pool reserves → what happens?
- Agent builds reputation then rug pulls → expected value of attack?
- Pool bank run scenario → how much buffer needed?

---

## Secondary Research (Important but not blocking MVP)

### 11. Regulatory Considerations
- Money transmitter licenses (if agents hold user funds)
- Insurance regulations (if running a pool)
- Securities law (are pool tokens securities?)
- International: how to handle cross-border transactions?

### 12. UX/UI Patterns
- How do users understand "your agent is staking ETH"?
- What's the right approval flow? (every transaction vs. spending limits)
- How to display reputation scores? (number, letter grade, emoji?)

### 13. Interoperability
- Can agents from different implementations talk to each other?
- Standard protocols for agent communication? (gRPC, GraphQL, custom?)
- How to handle versioning? (agent A uses v1, agent B uses v2)

### 14. Scaling & Infrastructure
- How many agents can one registry handle?
- RPC node requirements (read-heavy system)
- Indexing needs (The Graph, custom indexer?)
- CDN for agent metadata?

### 15. Business Model
- Who pays for development? (grants, token launch, fees?)
- How to sustain the project long-term?
- Open source vs. proprietary?

---

## Research Priorities

**Week 1-2**: 
- #1 (Reputation), #3 (LLM arbitration), #4 (EigenLayer)

**Week 3-4**: 
- #2 (Insurance pools), #5 (ERC-8004), #6 (L2 strategy)

**Month 2**: 
- #8 (Key management), #9 (Privacy), #10 (Economic modeling)

**Ongoing**: 
- #11 (Regulatory), #12 (UX), #13 (Interop)

---

## Key Uncertainties to Resolve

1. **Can multi-LLM arbitration be reliably gamed?** (If yes, entire dispute model fails)
2. **Does EigenLayer support this use case?** (If not, need alternative slashing mechanism)
3. **Can insurance pool pricing be algorithmic?** (If not, need manual underwriting = centralization)
4. **Is there product-market fit?** (Does anyone actually want this?)

Resolve these before building too much.
