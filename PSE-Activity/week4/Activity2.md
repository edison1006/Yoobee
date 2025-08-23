```mermaid
    flowchart TB
  %% Activity Diagram: Smart Task Manager (Two Main Activities)

  start([Start])

  %% Swimlanes via subgraphs
  subgraph A ["Activity A - Task Management"]
    A1["Open App"]
    A2{"Logged in user? (optional)"}
    A3["View Task List & Stats"]
    A4["Search/Filter by query/status/priority/tag"]
    A5{"Create / Edit / Delete / Toggle?"}
    A6["Create/Edit Task via Modal"]
    A7["Toggle Done/Undone"]
    A8["Delete Task"]
    A9["Update UI (cards, badges, progress bar)"]
  end

  subgraph B ["Activity B - Data Operations"]
    B1["Persist tasks to localStorage"]
    B2{"Import JSON?"}
    B3["Choose file -> Parse JSON"]
    B4["Replace current tasks"]
    B5{"Export JSON?"}
    B6["Download tasks-export.json"]
  end
  endx([End])

  %% Flow
  start --> A1 --> A2
  A2 -->|"Yes/Skip"| A3 --> A4 --> A5
  A2 -->|"No (optional auth later)"| A3

  A5 -->|"Create/Edit"| A6 --> A9
  A5 -->|"Toggle"| A7 --> A9
  A5 -->|"Delete"| A8 --> A9
  A5 -->|"None"| A9

  %% Data ops run whenever tasks change or user triggers import/export
  A9 --> B1
  B1 --> B2
  B2 -->|"Yes"| B3 --> B4 --> A3
  B2 -->|"No"| B5
  B5 -->|"Yes"| B6 --> A3
  B5 -->|"No"| A3

  A3 --> endx
