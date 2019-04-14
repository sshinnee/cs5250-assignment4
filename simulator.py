'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, process_id) indicating the time switching to that process_id
#Output_2 : Average Waiting Time
#return (["to be completed, scheduling process_list on round robin policy with time_quantum"], 0.0)
def RR_scheduling(process_list, time_quantum):
    schedule = [] #time, process_id
    current_time = 0
    waiting_time = 0
    #sort process list by arrival time in case input is not sorted
    process_list = sorted(process_list, key=lambda x: x.arrive_time)
    number_of_processes = len(process_list)

    while len(process_list) > 0:
        #process_id, arrival_time, burst_time
        #id, arrive_time, burst_time
        #filter out processes that have not yet arrived at this time point
        available_processes = [x for x in process_list if x.arrive_time <= current_time]
        if len(available_processes) == 0:
            current_time = current_time + time_quantum
            continue
        print 'current_time: ' + str(current_time)
        print '\tavailable_processes' 
        print '\t\t' + str(available_processes)
        process = available_processes[0]
        print '\tprocess chosen: ' + str(process)
        print '\tfirst process in process list: ' + str(process_list[0])
        schedule += [(current_time, process.id)]
        waiting_time = waiting_time + (current_time - process.arrive_time)
        if process.burst_time > time_quantum:
            process.burst_time = process.burst_time - time_quantum
            current_time = current_time + time_quantum
            process.arrive_time = current_time
            process_list.remove(process)
            process_list = process_list + [process]
            #print 'process_list'
            #print process_list
        else:
            process_list.remove(process)
            current_time = current_time + process.burst_time
            #print 'process_list'
            #print process_list
    average_waiting_time = waiting_time/float(number_of_processes)
    return (schedule, average_waiting_time)

#Input: process_list
#Output_1 : Schedule list contains pairs of (time_stamp, process_id) indicating the time switching to that process_id
#Output_2 : Average Waiting Time
def SRTF_scheduling(process_list):
    schedule = [] #time, process_id
    current_time = 0
    waiting_time = 0
    #sort process list by arrival time in case input is not sorted
    process_list = sorted(process_list, key=lambda x: x.arrive_time)
    number_of_processes = len(process_list)

    #while len(process_list) > 0:
    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

