# Delta Program Guide  

## Setup 
1. Ensure delta files follow as per folder naming convention (DD_MM_YYYY) for today date and yesterday date. Make sure to store csv in each folder . When automating file save, ensure to create a new folder with above naming convention and save each files in it. 
> Check in `main.py` if csv got any changes on first column nanme as it would affect changes tracking in line 14 where key = "col1" Change col1 to new first column name 
2. Run the program when both file are in respective folder . 
3. Running the program process: -
> In terminal, 
- create new python environment 
- Activate the environment 
- Run `pip install requirements.txt` to install all packages dependencies 
- Run the program `python main.py`
- Check the log files for any error if any 
- Check the delta folder for specific changes tracking 
4. To automate the process, ive create a script to automate the programm using shell script. 
>In terminal 
- `chmod +x run_script.sh`
- `crontab -e`
- `0 0 * * * /path/to/run_script.sh >> /path/to/script_log.log 2>&1`
- Run on midnight and if failed schedule to run again another 4 hours until succeed. 