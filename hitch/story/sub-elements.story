Sub-elements:
  docs: subelements
  about: |
    This example demonstrates both how to reference subelements (using subelements:)
    as well as how to select elements by selector and asking for the parent (using but parent:).
    
    It also shows how to grab these subelements - i.e. parent name / child name.
    
    This is an useful feature when grabbing things in groups or tables.
  based on: default
  given:
    selectors.yml: |
      dashboard:
        appears when: dashboard
        elements:
          dashboard: id=dashboard
          founder table:
            id: founder_table

            subelements:
              bill gates:
                text is: Bill Gates
                but parent: 1

                subelements:
                  age:
                    class: col_age

    website:
      index.html: |
        <div id="dashboard">
          <h4>Dashboard</h4>
          <table id="founder_table">
            <thead>
              <th>Name</th>
              <th>Age</th>
              <th>Company</th>
            </thead>
            <tbody>
            <tr>
              <td class="col_name">Bill Gates</td>
              <td class="col_age">35</td>
              <td class="col_company">Microsoft</td>
            </tr>
            <tr>
              <td class="col_name">Paul Allen</td>
              <td class="col_age">33</td>
              <td class="col_company">Microsoft</td>
            <tr>
            </tr>
              <td class="col_name">Steve Jobs</td>
              <td class="col_age">29</td>
              <td class="col_company">Apple</td>
            </tr>
            </tbody>
          </table>
        </div>

  steps:
  - Run: |
      selector.visit("http://localhost:8000")
      selector.wait_for_page("dashboard")
      selector.the("founder table / bill gates / age").should_contain("35")
