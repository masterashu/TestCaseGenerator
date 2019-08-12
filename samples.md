### Sample Code

* #### Generating Numbers  
  * Generate a Random Integer  
  `%d`
  * Generate a Random Integer less than **50**  
  `%d[:50]`
  * Generate a Random Integer more than **70**  
  `%d[-70:]`
  * Generate a Random Integer between **-10** - **30**  
  `%d[10:30]`
  * Generate the same Random Integer in the next line  
  `a:%d;$a`
  * Generate **10** Random Integers  
  `%d{10}`
  * Generate a Random Integer **n** followed by **n**    space seperated Integers in the next line  
  `a:%d;%d{$a}`
  * Generate three space seperated Random integers **10** no of times  
  `%(%d{3}){10}`
  * Generate a Random Integer **n** and a matrix of size **n** x **n** in **n** space seperated numbers in **n** lines  
  `n:%d;%(%d{$n}){$n}`






