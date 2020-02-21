* /
  * if logged in, redirect to /evaluations/
* /evaluations/schedule/
  * instructor only
  * form
    * team
    * date
    * series of checkboxes to choose topics to evaluate
* /evaluations/
  * student view
  * show previous evaluations and scheduled evaluations
* /evaluations/:pk/
  * student view
  * your evaluation from that date, review
* /evaluations/scheduled/:pk/
  * student view
  * form to fill out evaluation
    * for each topic, show radio buttons for each level
    * optimally, can save progress
* /evaluations/report/
  * student view
  * see a report of each evaluation you've done
* /evaluations/team/:pk/:date/
  * instructor view
  * see report for each topic 
    * distro of levels
    * with histogram?