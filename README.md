# **Wireframe Document Template**

### *(Formatted for Microsoft Word)*

---

# **TITLE PAGE**

**Project Name:** ______________________________________

**Document Title:** *Wireframe Document*
**Version:** v____
**Prepared By:** ________________________________
**Date:** ________________________________
**Client / Team:** ________________________________

(Optional: Add logo centered on page)

---

# **TABLE OF CONTENTS**

1. Introduction
2. Purpose of Document
3. Application Overview
4. Wireframe Conventions
5. Screen-by-Screen Wireframes
       5.1 Landing Page
       5.2 Intake Form
       5.3 Submission Confirmation
       5.4 Slot Selection
       5.5 Admin Review Screen
       5.6 Analytics Dashboard
6. Navigation Flow
7. Notes & Assumptions
8. Appendix

---

# **1. Introduction**

This document contains the low-fidelity wireframes for the ___________________ application. It outlines the screen layouts, content organization, and navigation structure prior to high-fidelity UI design or development.

The wireframes focus on **structure**, **function**, and **flow**, not visual styling.

---

# **2. Purpose of Document**

The purpose of this wireframe document is to:

* Provide early visualization of the application workflow
* Align stakeholders on expected screen behavior
* Define layout and element placement before development
* Serve as a foundation for UI/UX design and Power Apps implementation

---

# **3. Application Overview**

Provide a short description:

**Example:**
The Intake Portal Application enables users to submit, track, and manage AI/ML use cases. Admin users can review submissions, approve requests, assign meeting slots, and calculate estimated business value.

**Key Features:**

* New intake submission
* Slot selection
* Request tracking
* Admin review & approval workflow
* Dashboard analytics (BI integration)

**User Roles:**

* **User/Requester**
* **Admin/Reviewer**
* **Scheduler**

---

# **4. Wireframe Conventions**

Use these visual standards while interpreting wireframes:

| Element          | Meaning                                   |
| ---------------- | ----------------------------------------- |
| Grey Boxes       | Placeholder components / layout blocks    |
| Blue Boxes       | Buttons or interactive actions            |
| Dashed Boxes     | Containers or grouped elements            |
| Icons            | Functional placeholders, not final assets |
| Lorem ipsum text | Placeholder copy                          |

---

# **5. Screen-by-Screen Wireframes**

Each screen follows this structure.

---

## **5.1 Screen Name: Landing Page**

### **Purpose of Screen**

Describe what this screen does.

### **Wireframe Mockup**

*(Insert screenshot image here)*

### **Key UI Components**

1. **Header Section:** Contains navigation buttons (User Guide, FAQs, Learning Resources).
2. **Welcome Banner:** Displays user name and introductory text.
3. **Submit Button:** CTA for submitting new intake.
4. **Analytics Tiles:** Shows KPIs like Total Intakes, Approved Intakes, Estimated Value.
5. **Footer:** Shows app version and additional notes.

### **User Interactions**

* Click Submit → Navigate to Intake Form.
* Click FAQs → Navigate to FAQs page.
* Click Analytics → Opens Power BI dashboard.

### **Data Used**

* RequestID
* Status
* Estimated Business Value

---

## **5.2 Screen Name: Intake Form**

### **Purpose of Screen**

Describe the role of this screen.

### **Wireframe Mockup**

*(Insert screenshot)*

### **Components**

* Form fields (Title, Business Value, Description, LOB, Attachments)
* Submit button
* Cancel button

### **User Interactions**

* Submit → Saves record and triggers confirmation email.
* Cancel → Return to landing page.

---

## **5.3 Screen Name: Submission Confirmation**

### **Purpose**

To confirm successful submission.

### **Wireframe Mockup**

*(Insert screenshot)*

### **Components & Behavior**

* Success message
* RequestID display
* CTA to return to home

---

## **5.x Continue for all remaining screens**

* Slot Selection
* Admin Review
* Dashboard Page
* Profile Page

---

# **6. Navigation Flow**

Include a flow diagram or list:

* Landing Page → Intake Form → Confirmation
* Confirmation → Email Trigger → Slot Selection
* Slot Selection → Admin Approval → Final Status
* Admin → Dashboard → Analytics BI Page

---

# **7. Notes & Assumptions**

List assumptions made during design:

* User authentication handled by Azure AD
* Only approved users can access Admin screens
* Business Value is provided by user, validated by Admin
* Power BI dashboard updates every 30 minutes

---

# **8. Appendix**

* Glossary of terms
* Database table structure
* UI component library
* Color palette (if any)
* Future enhancements

---

**End of Wireframe Document Template**
