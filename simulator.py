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
from operator import attrgetter

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
#return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)
def SRTF_scheduling(process_list):
    schedule = [] #time, process_id
    current_time = 0
    waiting_time = 0
    current_process = None

    #sort process list by arrival time in case input is not sorted
    known_process_list = sorted(process_list, key=lambda x: x.arrive_time)
    number_of_processes = len(process_list)

    known_arrival_times = [x.arrive_time for x in process_list]

    waiting_processes = []

    number_of_waiting_processes = 0
    number_of_preemptive_processes = 0

    count = 0
    print('this is the known process list: ')
    for item in known_process_list:
        count += 1
        print(str(count) + ': ' + str(item))
    
    for next_process in known_process_list: 
        print('this is the current time: ' + str(current_time))
        print('these are the waiting processes: ' + str(waiting_processes))
        print('this is the next process: ' + str(next_process))
        #assert current_time == current_process.arrive_time
        if current_process == None:
            schedule += [(next_process.arrive_time, next_process.id)]
            print('added next process to schedule 0: ' + str(next_process))
            current_process = next_process
            current_time = current_process.arrive_time
            number_of_preemptive_processes += 1
            continue
        if next_process.arrive_time > current_time + current_process.burst_time:
            #next process has not yet arrived
            #current process will run to completion
            #current_time = current_time + current_process.burst_time
            #check waiting processes
            if len(waiting_processes) == 0:
                current_process = next_process
                current_time = current_process.arrive_time
                schedule += [(current_time, current_process.id)]
                print('\tlength of waiting processes is 0, added to schedule: ' + str(current_process))
                number_of_preemptive_processes += 1
                continue
            else:
                while len(waiting_processes) > 0:
                    #assert current_time == current_process.arrive_time
                    current_time = current_time + current_process.burst_time
                    current_process = min(waiting_processes, key=attrgetter('burst_time'))
                    waiting_processes.remove(current_process)
                    schedule += [(current_time, current_process.id)]
                    number_of_waiting_processes += 1
                    print('\tlength of waiting processes is > 0, added to schedule: ' + str(current_process))
                    waiting_time = waiting_time + (current_time - current_process.arrive_time)
                    print('\tthis process waited for: ' + str(current_time - current_process.arrive_time))
                    #current_time = current_time + current_process.burst_time
                    if next_process.arrive_time > current_time + current_process.burst_time:
                        #next process still has not arrived
                        print('\t\tcontinue through waiting processes: ' + str(waiting_processes))
                        if len(waiting_processes) == 0:
                            current_process = next_process
                            current_time = current_process.arrive_time
                            schedule += [(current_time, current_process.id)]
                            print('\t\t\tadded process to schedule (new arrival): ' + str(current_process))
                            number_of_preemptive_processes += 1
                        continue
                    else:
                        #next process has arrived
                        #current_time = next_process.arrive_time
                        current_process_left_time = current_time + current_process.burst_time - next_process.arrive_time
                        if next_process.burst_time < current_process_left_time:
                            #next process will pre-empt current process
                            print('\t\t\tcurrent time: ' + str(current_time))
                            print('\t\t\tcurrent process left time: ' + str(current_process_left_time))
                            print('\t\t\tcurrent process: ' + str(current_process))
                            schedule += [(next_process.arrive_time, next_process.id)]
                            number_of_preemptive_processes += 1
                            pre_empted_process = current_process
                            pre_empted_process.arrive_time = next_process.arrive_time
                            pre_empted_process.burst_time = current_process_left_time
                            waiting_processes += [pre_empted_process] 
                            print('\t\t\tadded this process to waiting: ' + str(pre_empted_process))
                            current_process = next_process
                            current_time = current_process.arrive_time
                            print('\t\t\tnext process pre-empts current one, added to schedule: ' + str(current_process))
                        else:
                            #next process does not pre-empt current process
                            waiting_processes += [next_process]
                            print('\t\t\tadded next process to waiting: ' + str(next_process))
                        print('\t\tbreak out of while loop: ' + str(waiting_processes))
                        break
            
                #waiting_processes += [next_process]

        else:
            #next process comes at a time when current process is still executing
            current_process_left_time = current_time + current_process.burst_time - next_process.arrive_time
            if next_process.burst_time < current_process_left_time:
                #next process will pre-empt current process
                print('current time 2: ' + str(current_time))
                print('current process left time 2: ' + str(current_process_left_time))
                print('current process 2: ' + str(current_process))
                schedule += [(next_process.arrive_time, next_process.id)]
                number_of_preemptive_processes += 1
                pre_empted_process = current_process
                pre_empted_process.arrive_time = next_process.arrive_time
                pre_empted_process.burst_time = current_process_left_time
                waiting_processes += [pre_empted_process] 
                print('added this process to waiting 2: ' + str(pre_empted_process))
                current_process = next_process
                current_time = current_process.arrive_time
                print('next process pre-empts current one, added to schedule 2: ' + str(current_process))
            else:
                #next process does not pre-empt current process
                waiting_processes += [next_process]
                print('added next process to waiting 2: ' + str(next_process))
            #current_process = next_process
            #current_time = current_process.arrive_time
        #current process is pre-empted

        #current process is not pre-empted
        #current_time = min(current_time + current_process.burst_time, next_arrival_time)
    #clear up all remaining waiting processes
    while len(waiting_processes) > 0:
        current_time = current_time + current_process.burst_time
        print('waiting list left: ' + str(waiting_processes))
        current_process = min(waiting_processes, key=attrgetter('burst_time'))
        waiting_processes.remove(current_process)
        schedule += [(current_time, current_process.id)]
        number_of_waiting_processes += 1
        print('added process from waiting to schedule: ' + str(current_process))
        print('this process waited for: ' + str(current_time - current_process.arrive_time))
        waiting_time = waiting_time + (current_time - current_process.arrive_time)
        
    print('total waiting time: ' + str(waiting_time))  
    print('total number of processes: ' + str(number_of_processes)) 
    print('total number of preemptive processes: ' + str(number_of_preemptive_processes))
    print('total number of waiting processes: ' + str(number_of_waiting_processes)) 
    #while len(process_list) > 0:
    return (schedule, waiting_time/float(number_of_processes))

#
#return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)
def SJF_scheduling(process_list, alpha):
    process_list = sorted(process_list, key=lambda x: x.arrive_time)
    #predicted_now = alpha*true_previous + (1-alpha)*predicted_previous
    predicted_cpu_burst_list = [5]*(len(process_list)+1)

    for i in range(0, len(process_list)):
        predicted_cpu_burst_list[i+1] = [alpha*process_list[i] + (1-alpha)*predicted_cpu_burst_list[i]]

    predicted_cpu_burst_list = predicted_cpu_burst_list[1:]
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
    process_list = read_input()
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    process_list = read_input()
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    process_list = read_input()
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

