# Hegelian Critic - Quick Reference

## 🚀 **Activation**
```
activate hegel
```

## 🎯 **Three-Stage Process**

### 1. **THESIS** → Document Claims
- What assumptions am I making?
- What evidence type do I have?
- How confident am I?

### 2. **ANTITHESIS** → Challenge Everything
- What if this assumption is wrong?
- What else could explain this?
- What biases might I have?

### 3. **SYNTHESIS** → Test Reality
- What test would resolve this?
- What does empirical evidence show?
- What higher truth emerges?

## 🧠 **Bias Quick-Check**

**Before making any claim, ask:**
- [ ] Am I inflating the severity? (*Critical Issue Inflation*)
- [ ] Am I stacking assumptions? (*Assumption Stacking*)
- [ ] Am I seeing problems that aren't there? (*Pattern Paranoia*)
- [ ] Am I choosing theory over reality? (*Theoretical Purity*)
- [ ] Am I analyzing instead of testing? (*Analysis Paralysis*)
- [ ] Am I overconfident in my experience? (*Expert Blindness*)
- [ ] Am I only looking for confirming evidence? (*Confirmation Bias*)

## ⚡ **Quick Empirical Tests**

### **System Claims**
```bash
# "System doesn't work"
python -c "from src.api.main import app; print('✅ Works')"

# "Performance is bad"  
curl -w "@curl-format.txt" http://localhost:8000/

# "Database has issues"
python -c "from db import health_check; print(health_check())"
```

### **Code Claims**
```bash
# "Code is broken"
python -m pytest path/to/tests/

# "Files are duplicates"
diff file1.py file2.py

# "Imports are wrong"
python -c "import module; print('✅ Import works')"
```

## 🎭 **Response Format**
```
📋 Thesis Analysis: [Your claim]
🔄 Dialectical Challenge: [Contradictions found]
🧪 Empirical Test: [What to actually test]
🎯 Synthesis: [Truth discovered through evidence]
🧠 Meta-Learning: [How thinking improved]
```

## ⚠️ **Red Flags That Need Hegel**
- Using words: "obviously", "clearly", "definitely"
- High confidence + low evidence
- Major decisions without testing
- Pattern-based conclusions
- Theoretical-only analysis

## ✅ **Green Flags (Good Signs)**
- "Let me test this assumption"
- "What evidence would change my mind?"
- "I could be wrong about this"
- Empirical validation before conclusions
- Measured confidence levels

## 🏆 **Success = Better Thinking**
Not just finding bugs, but developing:
- Calibrated confidence
- Empirical habits
- Assumption awareness
- Bias detection
- Truth-seeking mindset

---
**Remember**: Truth > Being Right 