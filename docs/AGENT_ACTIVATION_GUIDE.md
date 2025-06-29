# Luciq Agent Activation Guide

## 🧠 Discovery Enhancement Specialist

**Status**: ✅ **CREATED & READY FOR ACTIVATION**

### **Agent Location**
```
.cursor/mdc/discovery-enhancement-specialist.yml
```

### **Activation Instructions**

1. **Open Cursor IDE**
2. **Navigate to any trigger file**:
   - `apps/src/api/main.py` (discovery endpoint)
   - `data/processed-posts.json` (deduplication data)
   - `apps/src/prompts/discovery/` (prompt templates)
   - `ROADMAP_V2.md` (roadmap)
   - `SYSTEM_STATE_JUNE.md` (system docs)

3. **Activate the agent** by typing:
   ```
   Activate discovery-enhancement-specialist. Begin audit of scraping filters and scoring prompts.
   ```

### **Agent Capabilities**
- ✅ **Reddit Scraping Optimization**: Improve signal-to-noise ratio
- ✅ **LLM Prompt Engineering**: Refine pain point detection prompts
- ✅ **Scoring Enhancement**: Add confidence/impact calculations
- ✅ **Ranking Transparency**: Improve opportunity scoring logic
- ✅ **Subreddit Analysis**: Suggest new target communities

### **Current Discovery System Analysis**

#### **Existing Discovery Flow**:
1. **Reddit Scraping** → `pain_point_scraper_agent.py`
2. **Opportunity Ranking** → `opportunity_ranker.py`
3. **Concept Generation** → `concept_generator.py`
4. **Deduplication** → `processed-posts.json`
5. **Database Storage** → `saved_ideas` table

#### **Key Files to Enhance**:
- `apps/src/api/main.py` (lines 280-410) - Discovery endpoint
- `luciq/src/agents/pain_point_scraper_agent.py` - Reddit scraper
- `luciq/src/agents/opportunity_ranker.py` - Scoring logic
- `memory/pain-points-database.json` - Raw data
- `memory/ranked-opportunities.json` - Scored opportunities

### **Suggested First Tasks**
1. **Audit current Reddit scraping filters**
2. **Review LLM scoring prompts and rubrics**
3. **Analyze existing opportunity scores for patterns**
4. **Identify low-quality vs high-quality discoveries**
5. **Propose enhanced scoring methodology**

### **Test Data Available**
- ✅ **5 System Ideas** in database
- ✅ **Pain Points Database** with analyzed Reddit posts
- ✅ **Ranked Opportunities** with existing scores
- ✅ **Processed Posts** for deduplication testing

---

## **🚀 Quick Activation Command**

```bash
# In Cursor, open any trigger file and type:
Activate discovery-enhancement-specialist. Begin audit of scraping filters and scoring prompts.
```

**Expected Response**: Agent will analyze current discovery system and propose specific improvements to Reddit scraping, LLM prompts, and opportunity scoring logic. 