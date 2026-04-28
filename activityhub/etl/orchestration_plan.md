# Orchestration Plan for the Project

## Phase 1: Manual Tasks (Current Milestone)

### Survey Data Collection:
- **Task**: Manually design and distribute the survey using tools like Google Forms.
- **Reason for Manual**: Customization of questions and initial testing requires human oversight.
- **Automation in Future**: Post-survey, automation will trigger the data ingestion process into the database.

### Studio Data Collection:
- **Task**: Manually research and compile information on 20-30 local studios, including class types, schedules, prices, and locations.
- **Reason for Manual**: Data is location-specific and requires initial human effort to build a database of available studios.
- **Automation in Future**: Once the database is structured, data updates and additions can be automated through web scraping or APIs (e.g., using BeautifulSoup or Scrapy).

### Synthetic Data Generation:
- **Task**: Manually generate synthetic data (2,000-5,000 users) based on insights from the real survey data.
- **Reason for Manual**: Initial generation process will require manual analysis of real survey data patterns and distribution.
- **Automation in Future**: Synthetic data generation will be automated using libraries like Faker or SDV that follow pre-defined rules.

### Model Training & Validation:
- **Task**: Manually train the first iteration of the prediction model (logistic regression, random forest) using the collected survey and synthetic data.
- **Reason for Manual**: Initial experimentation with model selection and tuning requires manual intervention.
- **Automation in Future**: Training pipelines will be automated using orchestration tools like Apache Airflow, triggering model training automatically after data collection and preprocessing.

---

## Phase 2: Automated Tasks (Future Milestones)

### Data Ingestion Automation:
- **Task**: Automate the data ingestion process for survey responses, studio data, and synthetic user data.
- **Tools**: Use Apache Airflow to schedule and automate tasks like importing survey responses to the database and generating synthetic data.
- **Reason for Automation**: Once the data sources are stabilized, automating ingestion will reduce manual entry and speed up the process.

### Model Execution & Recommendation Generation:
- **Task**: Automate the model execution after new data ingestion to generate personalized recommendations.
- **Tools**: Use FastAPI for real-time execution of the trained model. Integrate with Apache Airflow to run the models on a batch basis or when new data is ingested.
- **Reason for Automation**: Continuous model execution without manual input is needed to provide real-time recommendations to users and studios.

### Scheduled Model Retraining:
- **Task**: Automate the retraining process of the model based on newly collected survey data or any user behavior data.
- **Tools**: Apache Airflow to schedule regular retraining of the model (e.g., monthly or quarterly).
- **Reason for Automation**: Retraining ensures that the model stays up-to-date with new patterns and trends in user behavior.

### Recommendation Insights for Studios:
- **Task**: Automatically generate and send insights to studios regarding customer segments and marketing effectiveness.
- **Tools**: PostgreSQL queries to retrieve insights and Email Automation (via Airflow or FastAPI) to send periodic reports.
- **Reason for Automation**: Studios will benefit from automated insights without needing to manually request them.

### Real-Time Recommendations for Users:
- **Task**: Implement real-time class and studio recommendations based on the user profile.
- **Tools**: FastAPI serving the model's recommendations, connected to the frontend via Streamlit.
- **Reason for Automation**: Real-time engagement with users can be automated to provide personalized suggestions as soon as users complete their onboarding quiz.

### Monitoring and Alerts:
- **Task**: Automate monitoring of the orchestration pipeline, and set up alerts if any task fails (e.g., model execution failure, data ingestion failure).
- **Tools**: Use Apache Airflow or Prefect for task monitoring and Slack/Email Notifications for real-time alerts.
- **Reason for Automation**: Continuous monitoring will help identify issues early and ensure a seamless process flow.

---

## Summary:

### Manual Tasks Now:
- Survey data collection, studio data collection, synthetic data generation, and initial model training.

### Automated Tasks in Future:
- Data ingestion, model execution, model retraining, recommendation generation, real-time user recommendations, and monitoring/alerts.
