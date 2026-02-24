# MVP: Agent Economy - Absolute Minimum Version

## Core Thesis to Prove
**"Two agents can transact with cryptographic guarantees and basic dispute resolution"**

That's it. Nothing else.

---

## What's IN the MVP

### 1. Two Agents (Hardcoded, No Registry)
```
User Agent (you control)
    ↕
Service Agent (also you control, simulating external service)
```

**No**:
- Agent discovery
- Multiple service providers
- Agent registry
- Semantic search
- Dynamic agent loading

**Yes**:
- Two Python scripts
- Hardcoded addresses
- Manual triggering

---

### 2. Simple L2 Transaction (One Testnet)
```
User Agent → sends request
Service Agent → provides service
Payment → settles on L2 (Base Sepolia or Arbitrum Sepolia)
```

**No**:
- Mainnet
- Multiple chains
- Complex pricing
- Dynamic gas estimation

**Yes**:
- Hardcoded service: "return current time" (trivial service)
- Fixed price: 0.001 ETH
- One L2 testnet
- Simple smart contract: escrow payment until service delivered

---

### 3. Basic Staking (Manual, No Slashing Yet)
```
Service Agent has staked 0.1 ETH in contract
This proves they have skin in the game
```

**No**:
- Dynamic stake calculation
- Automated slashing
- EigenLayer integration
- Reputation-based stake reduction

**Yes**:
- Hardcoded minimum stake: 0.1 ETH
- Manual stake deposit via CLI
- Check: does agent have stake? If no, transaction fails

---

### 4. Happy Path Only (No Disputes Yet)
```
1. User agent requests service
2. Service agent provides service
3. User agent verifies result
4. Payment released from escrow
5. Done
```

**No**:
- Dispute resolution
- Multi-LLM arbitration
- Slashing
- Appeals

**Yes**:
- Optimistic: assume both parties are honest
- Simple timeout: if service not delivered in X seconds, refund user
- Log everything to console

---

### 5. Conversation Hash (Not Encryption)
```
Conversation → hash with SHA-256 → store hash on-chain
```

**No**:
- Encryption
- IPFS storage
- Reveal mechanism
- Privacy guarantees

**Yes**:
- Prove conversation happened (via hash)
- Store hash in smart contract event log
- If dispute (future): could verify conversation matches hash

---

### 6. Manual Dispute (Human Decides)
```
If something goes wrong:
1. User or service agent raises flag (manual CLI command)
2. Transaction gets paused
3. Human (you) reviews logs
4. Human manually triggers refund or payment
```

**No**:
- Automated arbitration
- LLM judges
- On-chain voting
- Complex dispute logic

**Yes**:
- Escape hatch for when things go wrong
- Proves you can halt and reverse
- Manual review of what happened

---

## The Tech Stack (Minimalist)

### Smart Contracts
```solidity
// AgentEscrow.sol
contract AgentEscrow {
    mapping(address => uint256) public stakes;
    
    // Service agent stakes ETH
    function stake() external payable {
        require(msg.value >= 0.1 ether, "Minimum stake");
        stakes[msg.sender] += msg.value;
    }
    
    // User creates escrow for transaction
    function createTransaction(address serviceAgent) external payable returns (uint256) {
        require(stakes[serviceAgent] >= 0.1 ether, "Agent not staked");
        // Create transaction record
        // Hold payment in escrow
        // Return transaction ID
    }
    
    // Service agent delivers, user approves, payment released
    function completeTransaction(uint256 txId) external {
        // Verify service delivered (simple flag)
        // Release payment to service agent
        // Emit event with conversation hash
    }
    
    // Timeout: refund user if service not delivered
    function refundTransaction(uint256 txId) external {
        // Check timeout passed
        // Refund user
    }
    
    // Manual dispute resolution (owner only for MVP)
    function resolveDispute(uint256 txId, bool favorUser) external onlyOwner {
        // Manually resolve: refund user OR pay service agent
    }
}
```

### Agents (Python)
```python
# user_agent.py
class UserAgent:
    def request_service(self, service_agent_address):
        # 1. Create transaction on-chain (escrow payment)
        # 2. Send request to service agent (HTTP or direct call)
        # 3. Receive response
        # 4. Verify response (is it correct?)
        # 5. Approve transaction on-chain (release payment)
        # 6. Log conversation hash
        
# service_agent.py  
class ServiceAgent:
    def __init__(self):
        self.stake_amount = 0.1  # ETH
        
    def stake(self):
        # Deposit 0.1 ETH to contract
        
    def handle_request(self, request):
        # Provide service (e.g., return timestamp)
        # Submit result
        # Wait for payment
```

### Infrastructure
- **L2**: Base Sepolia (free testnet ETH, fast, low gas)
- **RPC**: Alchemy or Infura free tier
- **Wallet**: Hardcoded private keys (test keys only!)
- **LLM**: Not needed yet (no arbitration in MVP)

---

## User Flow (Manual, Command-Line)

```bash
# Terminal 1: Service Agent
$ python service_agent.py stake
> Staking 0.1 ETH...
> Staked! Address: 0xABC...

$ python service_agent.py listen
> Listening for requests...

# Terminal 2: User Agent  
$ python user_agent.py request-service 0xABC... "get-timestamp"
> Creating transaction...
> Escrowing 0.001 ETH...
> Requesting service from 0xABC...
> Received: {"timestamp": "2026-02-22T10:30:00Z"}
> Verifying response... ✓
> Approving payment...
> Transaction complete!
> Conversation hash: 0x789...
```

---

## Success Criteria

**The MVP is successful if**:

1. ✅ Two agents can transact on testnet L2
2. ✅ Service agent must stake before operating
3. ✅ Payment is held in escrow until service delivered
4. ✅ Conversation is hashed and logged on-chain
5. ✅ Timeout refund works if service agent disappears
6. ✅ Manual dispute resolution works (human can intervene)

**Time to build**: 2-4 weeks for one developer

---

## What's Explicitly OUT of Scope

❌ Agent registry  
❌ Reputation system  
❌ Insurance pools  
❌ Automated slashing  
❌ Multi-LLM arbitration  
❌ EigenLayer integration  
❌ Privacy/encryption  
❌ Multiple service types  
❌ UI/UX (command-line only)  
❌ Multiple users (just you testing)  
❌ Mainnet deployment  
❌ Token economics  
❌ Governance  

---

## Next Steps After MVP Works

**Version 0.2**: Add basic reputation
- Count successful transactions per agent
- Display score
- Adjust stake requirements based on score

**Version 0.3**: Add simple dispute resolution
- User can flag transaction as disputed
- Single LLM reviews conversation
- Automated slash/refund based on verdict

**Version 0.4**: Add insurance pool
- Simple pool: anyone can deposit
- Fixed premium: 2% of transaction
- Pay out on disputes

**Version 0.5**: Add agent registry
- Agents can register themselves
- Basic metadata (name, services offered)
- Search by service type

---

## Why This MVP?

**Tests the core assumptions**:
1. Can agents hold keys and transact? ✓
2. Does escrow + stake provide security? ✓
3. Is on-chain settlement feasible? ✓
4. Can we log conversations for later verification? ✓

**Doesn't waste time on**:
- Complex mechanisms that might not be needed
- Perfect UX before product-market fit
- Infrastructure that doesn't matter yet (multi-chain, decentralization)

**Validates**:
- Technical feasibility (smart contracts work, agents can interact)
- Economic model (stake + escrow = basic trust)
- User experience (is this actually usable, even in rough form?)

---

## The Pitch After MVP

If MVP works, you can show:

> "Here are two agents transacting with cryptographic guarantees. 
> Service agent has staked ETH (skin in the game).
> Payment is atomic (escrow until delivered).
> Conversation is logged (verifiable if dispute).
> This works on L2 with sub-$0.01 fees and sub-second finality.
> 
> Now imagine this with:
> - Thousands of service agents
> - Automated dispute resolution
> - Reputation-based trust
> - Insurance pools backing high-value transactions
> - No middlemen, no banks, no platforms
> 
> That's the vision. The MVP proves it's possible."

Then raise funding / recruit team / build for real.

---

## Timeline

**Week 1**: Smart contracts + deployment
**Week 2**: Basic agents (stake, request, deliver)
**Week 3**: Escrow flow + happy path
**Week 4**: Timeout + manual dispute, testing, demo

**Deliverable**: Working demo video + code on GitHub
