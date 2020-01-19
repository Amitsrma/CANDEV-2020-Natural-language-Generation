# CANDEV-2020-Natural-language-Generation
This is the attempt we made towards solving the challenge. We went mechanical over Language generation instead of using Neural Network or N-grams or skip-grams because of one of the requirements which stated that our result should be legible and perfect.
Our process on data analysis included:
<ol>
  <li>Downloaded the data from statcan website.</li>
  <li>Removed columns that were irrelevant.</li>
  <li>Original data had sales values over different locations (Cities) for different time (YYYY-MM).</li>
  <li>Original data was grouped by date and summed over it. This gave the sales of different sectors in Canada.</li>
  <li>From this sales amount, we calculated successive changes and kept track of successive increasing and decreasing of sales.</li>
</ol>

<h3>Following image shows the distribution of sales across different cities</h2>

![alt text](https://raw.githubusercontent.com/Amitsrma/CANDEV-2020-Natural-language-Generation/master/Final%20Dashboard.png)
