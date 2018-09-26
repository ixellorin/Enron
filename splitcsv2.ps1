# variable used to store the path of the source CSV file
$sourceCSV = 'C:\Users\Cio\Documents\Enron\emails.csv' ;

# variable used to advance the number of the row from which the export starts
$startrow = 0 ;

# counter used in names of resulting CSV files
$counter = 1 ;

# setting the while loop to continue as long as the value of the $startrow variable is smaller than the number of rows in your source CSV file
while ($startrow -lt 500000)
{

# import of however many rows you want the resulting CSV to contain starting from the $startrow position and export of the imported content to a new file
Import-CSV $sourceCSV | select-object -skip $startrow -first 1 | Export-CSV "C:\Users\Cio\Documents\Enron\small_email_set_$($counter).csv" -NoClobber;

# advancing the number of the row from which the export starts
$startrow += 10000 ;

# incrementing the $counter variable
$counter++ ;

}
