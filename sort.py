import numpy as np

def sort(onset,offset,pitch_shift):
    '''
    sorts onset and offset times while tracking the type of event
    returns: event_time, event_type
    '''
    event_type = []
    event_time = []
    for on in onset:
        event_type.append("on")
        event_time.append(on)
    for off in offset:
        event_type.append("off")
        event_time.append(off)
    for pitch in pitch_shift:
        event_type.append("pitch")
        event_time.append(pitch)
    #print(event_time)
    #print(event_type)
    if len(event_time) != len(event_type):
        raise Exception('arrays not the same length')
    else:
        quickSortHelper(event_time,event_type,0,len(event_time)-1)
    return event_time,event_type

#quicksort basic code from pythoncentral.io
def quickSortHelper(event_time,event_type,first,last):

  if first<last:
      splitpoint = partition(event_time,event_type,first,last)
      quickSortHelper(event_time,event_type,first,splitpoint-1)
      quickSortHelper(event_time,event_type,splitpoint+1,last)

def partition(event_time,event_type,first,last):

  pivotvalue = event_time[first]
  leftmark = first+1
  rightmark = last
  done = False

  while not done:
      while leftmark <= rightmark and event_time[leftmark] <= pivotvalue:
          leftmark = leftmark + 1

      while event_time[rightmark] >= pivotvalue and rightmark >= leftmark:
          rightmark = rightmark -1

      if rightmark < leftmark:
          done = True
      else:
          temp = event_time[leftmark]
          event_time[leftmark] = event_time[rightmark]
          event_time[rightmark] = temp
          temp2 = event_type[leftmark]
          event_type[leftmark] = event_type[rightmark]
          event_type[rightmark] = temp2

  temp = event_time[first]
  event_time[first] = event_time[rightmark]
  event_time[rightmark] = temp
  temp2 = event_type[first]
  event_type[first] = event_type[rightmark]
  event_type[rightmark] = temp2

  return rightmark    