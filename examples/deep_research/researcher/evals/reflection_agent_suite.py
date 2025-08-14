import json

reflection_agent_test_suite = [
    # 1. Low iteration count (<2), knowledge seems sufficient -> should CONTINUE
    {
        "id": "reflect_continue_low_iter_sufficient",
        "prompt": json.dumps(
            {
                "research_topic": "The impact of AI on the job market",
                "current_questions": [],  # Assuming they were just answered
                "gathered_knowledge": [
                    {
                        "query": "historical impacts",
                        "content": "Tech revolutions displace workers but create new job categories long-term.",
                    },
                    {
                        "query": "affected sectors",
                        "content": "Manufacturing and data entry are heavily affected, while creative jobs are less so.",
                    },
                ],
                "current_iteration": 1,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    # 2. Max iterations reached, knowledge is insufficient -> should STOP
    {
        "id": "reflect_stop_max_iterations",
        "prompt": json.dumps(
            {
                "research_topic": "The benefits of a Mediterranean diet",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "components",
                        "content": "Rich in fruits, vegetables, olive oil.",
                    }
                ],
                "current_iteration": 3,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": True,
    },
    # 3. Sufficient knowledge, not at max iterations -> should STOP
    {
        "id": "reflect_stop_sufficient_knowledge",
        "prompt": json.dumps(
            {
                "research_topic": "The history of the Roman Empire",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "rise",
                        "content": "Rose due to military, Senate, and integration.",
                    },
                    {
                        "query": "transition to empire",
                        "content": "Civil wars and powerful generals like Caesar led to the Empire.",
                    },
                    {
                        "query": "fall",
                        "content": "Fell due to invasions, economic troubles, and corruption.",
                    },
                ],
                "current_iteration": 2,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": True,
    },
    # 4. Insufficient knowledge, not at max iterations -> should CONTINUE
    {
        "id": "reflect_continue_insufficient_knowledge",
        "prompt": json.dumps(
            {
                "research_topic": "The process of photosynthesis",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "What is photosynthesis?",
                        "content": "Photosynthesis is the process used by plants to convert light energy into chemical energy.",
                    }
                ],
                "current_iteration": 2,
                "max_iterations": 4,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    # 5. Empty knowledge, not at max iterations -> should CONTINUE
    {
        "id": "reflect_continue_empty_knowledge",
        "prompt": json.dumps(
            {
                "research_topic": "The life cycle of a star",
                "current_questions": [],
                "gathered_knowledge": [],
                "current_iteration": 1,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    # 6. Borderline knowledge with clear gaps -> should CONTINUE
    {
        "id": "reflect_continue_borderline_gaps",
        "prompt": json.dumps(
            {
                "research_topic": "The impact of remote work on employee well-being",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "productivity",
                        "content": "Studies show mixed results on productivity, with some reporting increases and others decreases.",
                    },
                    {
                        "query": "communication",
                        "content": "Remote work relies heavily on digital communication tools, which can lead to 'Zoom fatigue'.",
                    },
                ],
                "current_iteration": 2,
                "max_iterations": 4,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    # 7. Very comprehensive knowledge -> should STOP
    {
        "id": "reflect_stop_very_comprehensive",
        "prompt": json.dumps(
            {
                "research_topic": "Key Battles of the American Civil War",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "Gettysburg",
                        "content": "A major Union victory, turning point of the war. Lasted three days.",
                    },
                    {
                        "query": "Antietam",
                        "content": "Bloodiest single day in American history. Allowed Lincoln to issue the Emancipation Proclamation.",
                    },
                    {
                        "query": "Vicksburg",
                        "content": "Gave the Union control of the Mississippi River, splitting the Confederacy.",
                    },
                ],
                "current_iteration": 2,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": True,
    },
    # 8. Max iterations is 1, knowledge is lacking -> should STOP
    {
        "id": "reflect_stop_max_iter_is_one",
        "prompt": json.dumps(
            {
                "research_topic": "The process of photosynthesis",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "What is it?",
                        "content": "It is a process to convert light to energy.",
                    }
                ],
                "current_iteration": 1,
                "max_iterations": 1,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": True,
    },
    # 9. Iteration is 0 (first reflection) -> should CONTINUE
    {
        "id": "reflect_continue_iter_zero",
        "prompt": json.dumps(
            {
                "research_topic": "The life cycle of a star",
                "current_questions": [],
                "gathered_knowledge": [],
                "current_iteration": 0,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    # 10. Nuanced gaps in knowledge -> should CONTINUE
    {
        "id": "reflect_continue_nuanced_gaps",
        "prompt": json.dumps(
            {
                "research_topic": "Compare and contrast Python and JavaScript for web development",
                "current_questions": [],
                "gathered_knowledge": [
                    {
                        "query": "Python backend",
                        "content": "Python is strong on the backend with frameworks like Django and Flask.",
                    },
                    {
                        "query": "JS frontend",
                        "content": "JavaScript dominates the frontend with libraries like React, Vue, and Angular.",
                    },
                ],
                "current_iteration": 2,
                "max_iterations": 3,
            },
            indent=2,
        ),
        "expected_additional_questions_empty": False,
    },
    {
        "id": "complex_pandemic_timeline_insufficient_research",
        "prompt": """Research Topic: Provide a detailed account of the first six months of the pandemic, highlighting key events such as virus discovery, initial transmission patterns, early public health interventions, and evolving global responses during this period.
Current research data:
[
  {
    "content": "The first six months of the COVID-19 pandemic were marked by a series of critical events that shaped the global response to the emerging health crisis. Below is a timeline highlighting key developments from December 2019 to June 2020:\\n\\n**December 2019**\\n\\n- **December 8**: The first known patient in Wuhan, China, begins experiencing symptoms of what would later be identified as COVID-19. ([weforum.org](https://www.weforum.org/agenda/2020/04/coronavirus-spread-covid19-pandemic-timeline-milestones/?utm_source=openai))\\n\\n- **December 31**: Chinese authorities report a cluster of pneumonia cases of unknown cause to the World Health Organization (WHO). ([who.int](https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai))\\n\\n**January 2020**\\n\\n- **January 1**: WHO activates its Incident Management Support Team across all levels—country, regional, and headquarters—to coordinate the response. ([who.int](https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai))\\n\\n- **January 7**: Chinese scientists identify a novel coronavirus as the cause of the outbreak. ([who.int](https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai))\\n\\n- **January 13**: The first confirmed case outside China is reported in Thailand. ([who.int](https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai))\\n\\n- **January 20**: China's National Health Commission confirms human-to-human transmission of the virus. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_January_2020?utm_source=openai))\\n\\n- **January 30**: WHO declares the outbreak a Public Health Emergency of International Concern (PHEIC). ([who.int](https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai))\\n\\n**February 2020**\\n\\n- **February 2**: The first death outside China occurs in the Philippines. ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC9114873/?utm_source=openai))\\n\\n- **February 5**: The U.S. Centers for Disease Control and Prevention (CDC) begins shipping diagnostic test kits to state and local health agencies; however, issues with these kits impede timely detection and response. ([axios.com](https://www.axios.com/2020/04/10/coronavirus-timeline-trump-administration-testing?utm_source=openai))\\n\\n**March 2020**\\n\\n- **March 11**: WHO declares COVID-19 a pandemic, expressing concern over \\\"the alarming levels of inaction.\\\" ([keystonekeynote.com](https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai))\\n\\n- **March 13**: U.S. President Donald Trump declares a national emergency, unlocking billions of dollars in federal funding to combat the virus. ([keystonekeynote.com](https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai))\\n\\n- **March 19**: California becomes the first U.S. state to issue a statewide stay-at-home order. ([keystonekeynote.com](https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai))\\n\\n**April 2020**\\n\\n- **April 6**: By this date, 42 U.S. states have imposed stay-at-home orders as the administration continues to battle the crisis. ([axios.com](https://www.axios.com/2020/04/10/coronavirus-timeline-trump-administration-testing?utm_source=openai))\\n\\n**May 2020**\\n\\n- **May 28**: COVID-19 deaths in the United States surpass 100,000. ([keystonekeynote.com](https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai))\\n\\n**June 2020**\\n\\n- **June 10**: COVID-19 cases in the United States reach 2 million. ([keystonekeynote.com](https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai))\\n\\nThese events underscore the rapid progression of the pandemic and the varied responses by global health authorities and governments during its initial phase.\\n\\n\\n## Key Developments in the Early COVID-19 Response:\\n- [Timeline: How the U.S. fell behind on the coronavirus](https://www.axios.com/2020/04/10/coronavirus-timeline-trump-administration-testing?utm_source=openai)\\n- [The Trump Administration Fumbled Its Initial Response to Coronavirus. Is There Enough Time to Fix It?](https://time.com/5805683/trump-administration-coronavirus/?utm_source=openai)\\n- [A timeline of Fauci's predictions about the COVID pandemic](https://www.axios.com/2022/04/27/covid-timeline-told-through-fauci-predictions?utm_source=openai)",
    "source": "weforum.org, who.int, en.wikipedia.org, pmc.ncbi.nlm.nih.gov, axios.com, keystonekeynote.com, The Trump Administration Fumbled Its Initial Response to Coronavirus. Is There Enough Time to Fix It?, A timeline of Fauci's predictions about the COVID pandemic",
    "url": "https://www.weforum.org/agenda/2020/04/coronavirus-spread-covid19-pandemic-timeline-milestones/?utm_source=openai, https://www.who.int/news/item/27-04-2020-who-timeline---covid-19/?utm_source=openai, https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_January_2020?utm_source=openai, https://pmc.ncbi.nlm.nih.gov/articles/PMC9114873/?utm_source=openai, https://www.axios.com/2020/04/10/coronavirus-timeline-trump-administration-testing?utm_source=openai, https://keystonekeynote.com/2669/forum/the-world-today/covid-19-a-one-year-timeline/?utm_source=openai, https://time.com/5805683/trump-administration-coronavirus/?utm_source=openai, https://www.axios.com/2022/04/27/covid-timeline-told-through-fauci-predictions?utm_source=openai",
    "query": "What were the key events in the discovery and initial response to the virus during the first six months of the pandemic?"
  },
  {
    "content": "In the initial six months of the COVID-19 pandemic, the virus exhibited rapid human-to-human transmission, primarily through respiratory droplets and close contact. Early studies indicated that the basic reproduction number (R₀) in Wuhan, China, ranged between 1.6 and 2.6 in January 2020, suggesting that each infected individual could spread the virus to approximately two others. ([thelancet.com](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099%2820%2930144-4/fulltext?utm_source=openai))\\n\\nTo curb the spread, various countries implemented a range of non-pharmaceutical interventions (NPIs):\\n\\n- **Travel Restrictions and Lockdowns**: China imposed a travel ban on Wuhan on January 23, 2020, and enforced strict lockdowns in the city and other regions. These measures significantly reduced transmission rates, with studies estimating a 96% reduction in cases outside Wuhan by February 19, 2020, compared to scenarios without interventions. ([science.org](https://www.science.org/doi/full/10.1126/science.abb6105?utm_source=openai))\\n\\n- **Quarantine and Isolation**: Quarantine measures, including stay-at-home orders and isolation of confirmed cases, were widely adopted. Mathematical models suggest that without such measures, cumulative confirmed cases could have been substantially higher within 40 days after lockdowns in cities like Wuhan, New York, Milan, and London. ([arxiv.org](https://arxiv.org/abs/2202.05176?utm_source=openai))\\n\\n- **Social Distancing**: Reducing interpersonal contacts was crucial. Studies reported a 65%–87% reduction in mean daily contacts during initial mitigation periods, correlating with decreased transmission rates. ([journals.lww.com](https://journals.lww.com/epidem/fulltext/2021/11000/rapid_review_of_social_contact_patterns_during_the.3.aspx?utm_source=openai))\\n\\n- **Mask-Wearing**: Widespread use of face masks was effective in reducing transmission. A systematic review and meta-analysis found that mask-wearing cuts the incidence of COVID-19 by 53% overall. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Public_health_mitigation_of_COVID-19?utm_source=openai))\\n\\n- **Community-Wide Screening and Testing**: Routine testing and community-wide screening helped identify asymptomatic cases, enabling timely isolation and reducing community transmission. For instance, China conducted extensive PCR testing during outbreaks to detect and isolate infected individuals promptly. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Zero-COVID?utm_source=openai))\\n\\nThese combined measures were instrumental in mitigating the spread of COVID-19 during the early stages of the pandemic.",
    "source": "thelancet.com, science.org, arxiv.org, journals.lww.com, en.wikipedia.org, en.wikipedia.org",
    "url": "https://www.thelancet.com/journals/laninf/article/PIIS1473-3099%2820%2930144-4/fulltext?utm_source=openai, https://www.science.org/doi/full/10.1126/science.abb6105?utm_source=openai, https://arxiv.org/abs/2202.05176?utm_source=openai, https://journals.lww.com/epidem/fulltext/2021/11000/rapid_review_of_social_contact_patterns_during_the.3.aspx?utm_source=openai, https://en.wikipedia.org/wiki/Public_health_mitigation_of_COVID-19?utm_source=openai, https://en.wikipedia.org/wiki/Zero-COVID?utm_source=openai",
    "query": "How did early transmission patterns evolve, and what measures were taken to mitigate the spread in the first six months?"
  },
  {
    "content": "In the first half of 2025, the global community undertook significant collaborative efforts to address various health crises, leading to notable impacts on containment and prevention measures.\\n\\n**Emergency Medical Deployments and Supplies**\\n\\nThe World Health Organization (WHO) played a pivotal role by deploying 89 emergency medical teams and delivering specialist medical supplies valued at US$ 196 million to 80 countries. These interventions were crucial in managing outbreaks and providing essential healthcare services in affected regions. ([who.int](https://www.who.int/news-room/speeches/item/report-of-the-director-general-to-member-states-at-the-seventy-eighth-world-health-assembly-19-may-2025?utm_source=openai))\\n\\n**Cholera Outbreak Management**\\n\\nCholera outbreaks were brought under control in 27 of 33 affected countries, with only six remaining in an acute phase. This success was attributed to coordinated international responses, including vaccination campaigns and improved sanitation measures. ([who.int](https://www.who.int/news-room/speeches/item/report-of-the-director-general-to-member-states-at-the-seventy-eighth-world-health-assembly-19-may-2025?utm_source=openai))\\n\\n**Marburg Virus and Ebola Containment**\\n\\nWith WHO support, Rwanda and Tanzania successfully halted Marburg virus disease outbreaks. Similarly, Uganda managed to stop an Ebola outbreak, initiating a vaccine trial within four days of detection, demonstrating the effectiveness of rapid response and international cooperation. ([who.int](https://www.who.int/news-room/speeches/item/report-of-the-director-general-to-member-states-at-the-seventy-eighth-world-health-assembly-19-may-2025?utm_source=openai))\\n\\n**Mpox Vaccination Efforts**\\n\\nIn response to mpox outbreaks, WHO granted Emergency Use Listing to the first mpox vaccines and tests, coordinating the donation of six million vaccine doses across 15 countries. This initiative was instrumental in controlling the spread of the disease. ([who.int](https://www.who.int/news-room/speeches/item/report-of-the-director-general-to-member-states-at-the-seventy-eighth-world-health-assembly-19-may-2025?utm_source=openai))\\n\\n**Polio Vaccination Campaigns**\\n\\nAn emergency polio campaign in the Gaza Strip vaccinated over 550,000 children, preventing a resurgence of the disease. This effort underscored the importance of maintaining immunization programs even in conflict zones. ([who.int](https://www.who.int/director-general/speeches/detail/who-director-general-s-opening-remarks-at-the-156th-session-of-the-executive-board-3-february-2025?utm_source=openai))\\n\\n**Pandemic Preparedness and Financing**\\n\\nThe adoption of the historic Pandemic Agreement at the Seventy-eighth World Health Assembly marked a global commitment to strengthening future preparedness through equitable access to vaccines and countermeasures. Additionally, the United States pledged up to $667 million by 2025 to support the Pandemic Fund, aiming to enhance pandemic prevention and response capabilities in low- and middle-income countries. ([who.int](https://www.who.int/news/item/25-06-2025-momentum-builds-to-protect-immunization-post-world-health-assembly?utm_source=openai), [whitehouse.gov](https://www.whitehouse.gov/briefing-room/statements-releases/2024/12/11/fact-sheet-biden-harris-administration-releases-global-health-security-annual-report-demonstrating-the-impact-of-united-states-leadership-and-investments/?utm_source=openai))\\n\\n**Immunization Initiatives**\\n\\nThe World Health Assembly established World Cervical Cancer Elimination Day on 17 November to promote actions against the disease, including increasing access to human papillomavirus (HPV) vaccines. This initiative highlights the ongoing global efforts to eliminate vaccine-preventable diseases. ([who.int](https://www.who.int/news/item/04-06-2025-global-health-leaders-urge-action-on-immunization-priorities-at-seventy-eighth-world-health-assembly?utm_source=openai))\\n\\nThese collective actions during the first half of 2025 significantly bolstered global health security, improved outbreak containment, and reinforced the importance of international collaboration in addressing health emergencies.",
    "source": "who.int, who.int, who.int, whitehouse.gov, who.int",
    "url": "https://www.who.int/news-room/speeches/item/report-of-the-director-general-to-member-states-at-the-seventy-eighth-world-health-assembly-19-may-2025?utm_source=openai, https://www.who.int/director-general/speeches/detail/who-director-general-s-opening-remarks-at-the-156th-session-of-the-executive-board-3-february-2025?utm_source=openai, https://www.who.int/news/item/25-06-2025-momentum-builds-to-protect-immunization-post-world-health-assembly?utm_source=openai, https://www.whitehouse.gov/briefing-room/statements-releases/2024/12/11/fact-sheet-biden-harris-administration-releases-global-health-security-annual-report-demonstrating-the-impact-of-united-states-leadership-and-investments/?utm_source=openai, https://www.who.int/news/item/04-06-2025-global-health-leaders-urge-action-on-immunization-priorities-at-seventy-eighth-world-health-assembly?utm_source=openai",
    "query": "What were the major global responses and collaborations during the first six months, and how did they impact containment efforts?"
  }
]
Current iteration: 1
Max iterations: 2""",
        "expected_additional_questions_empty": False,
    },
]

reflection_agent_criteria = """
**1. JSON Structure**: The output must be a valid JSON object with exactly two fields: 'additional_questions' (list) and 'reasoning' (string). No other fields like 'state_name' should be present.

**2. Additional Questions Logic**: The reflection agent must correctly determine when to continue or stop research:
   - If the research should continue, the 'additional_questions' list must contain between 1 and 3 non-empty research questions.
   - If the research should stop, the 'additional_questions' list must be empty.
   - Expected behavior is indicated by the 'expected_additional_questions_empty' field in each test case.

**3. Question Quality**: When 'additional_questions' is non-empty, the questions must be:
   - Specific and focused research questions that address knowledge gaps
   - Different from existing questions that were already researched
   - Relevant to exploring deeper aspects of the research topic

**4. Reasoning Quality**: The 'reasoning' field must be a non-empty string that logically justifies the decision, considering factors like:
   - Current iteration vs max iterations
   - Scope and complexity of the research topic
   - Adequacy of gathered knowledge relative to the topic's requirements
   - Identification of specific knowledge gaps

**5. Complex Topic Assessment**: For complex, multi-faceted topics like "the first six months of a worldwide pandemic" with minimal research completed (current_iteration much less than max_iterations), the agent should recognize that more research is needed and generate additional questions unless max_iterations is reached."""
