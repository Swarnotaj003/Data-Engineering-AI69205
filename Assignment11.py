""""
ASSIGNMENT 11

The academic office is redesigning the M.Tech curriculum. Every course may list
prerequisites: a course can only be taken after all of its prerequisites are completed.
Faculty committees keep adding prerequisite rules independently, as a result, the rules
can contradict each other: course A requires B, B requires C, and C requires A. A student
advised into any of these courses can never take it, because each one waits on another
that can never be taken first. 

You need to write a python program that will help the students. Thus, given the list 
of courses and prerequisite rules, your program must do thefollowing:
    1. Produce a valid order in which a student can take every course.
    2. Detect when the rules are contradictory (a cycle) and report exactly which courses
    form the loop, so the committee can fix it.

Implement an algorithm in python. Submit this as single .py file (with two functions)
with the name format: <assgn-11-roll.py>.
Input data format:
• Line 1: two integers n and m (number of courses, number of prerequisite rules).
• Next n lines: one course code per line
• Next m lines: two codes A B, meaning course A must be completed before course B.

Sample data and expected output is given in the data.txt file.
"""

class CourseOrder:
    def __init__(self, filename):
        self.n_courses = 0         
        self.n_prerequisites = 0
        self.adjlist = {}
        self._read_graph(filename)

    def _read_graph(self, filename):
        """
        Construct adjacency list representation of the directed 
        graph whose nodes and edges are given in the text file.
        """
        try:
            with open(filename, 'r') as file:
                self.n_courses, self.n_prerequisites = map(int, file.readline().split())

                for i in range(self.n_courses):
                    course = file.readline().strip()
                    self.adjlist[course] = []

                for j in range(self.n_prerequisites):
                    course_a, course_b = file.readline().split()
                    self.adjlist[course_a].append(course_b)

        except Exception as e:
            print(f"ERROR in parsing input file! Path: {filename}")
            print(e)

    def get_valid_course_order(self):
        """
        Produce a valid order in which a student can take every course,
        by performing topological sort using Kahn's algorithm.
        """
        indegree = {}   # count of incoming edges (prerequisites)
        
        for course in self.adjlist:
            indegree[course] = 0

        for course_a in self.adjlist:
            for course_b in self.adjlist[course_a]:
                indegree[course_b] += 1

        # collect no-prerequisite courses
        queue = [course for course in indegree if indegree[course] == 0]
        course_order = []

        while len(queue) > 0:
            course = queue.pop(0)
            course_order.append(course)

            # release subsequent courses
            for next_course in self.adjlist[course]:
                indegree[next_course] -= 1
                # if next_course meets all prerequisites till now
                if indegree[next_course] == 0:
                    queue.append(next_course)

        if len(course_order) < self.n_courses:
            return None     # prerequisites has at least one cycle
        return course_order

    def get_contradicting_courses(self):
        """
        Report which courses form prerequisite loop,
        by detecting all cycles using Tarjan's algorithm.
        """
        clock = 0
        cycles = []     

        # state tracking vectors
        disc = {}       # discovery time
        low = {}        # head of scc/cycle (lowest disc of the cycle)
        on_stk = {}
        stk = []

        for course in self.adjlist:
            disc[course] = -1
            low[course] = -1
            on_stk[course] = False

        def scc_dfs(course):
            nonlocal clock

            # mark the course as visited
            stk.append(course)
            on_stk[course] = True
            disc[course] = low[course] = clock
            clock += 1

            for next_course in self.adjlist[course]:
                if disc[next_course] == -1:  
                    # unvisited neighbor   
                    scc_dfs(next_course)
                    low[course] = min(low[course], low[next_course])
                elif on_stk[next_course]:   
                    # back edge, cycle found
                    low[course] = min(low[course], disc[next_course])    

            # if we're at the head of a SCC (cycle)
            if disc[course] == low[course]:
                scc = []
                while True:
                    node = stk.pop()
                    on_stk[node] = False
                    scc.append(node)
                    if node == course:
                        break

                # valid cycle: atleast 2 courses or self loop
                if len(scc) > 1 or course in self.adjlist[course]:
                    cycles.append(scc)

        # run dfs for all unconnected courses
        for course in self.adjlist:
            if disc[course] == -1:      # if unvisited
                scc_dfs(course)

        return cycles


if __name__ == "__main__":
    filename = input("Enter input file path for the courses: ")
    co = CourseOrder(filename)
    course_order = co.get_valid_course_order()
    cycles = co.get_contradicting_courses()

    print("One of the valid orders:", course_order)

    if len(cycles) > 0:
        print("Courses with contradicting prerequisites:")
        for i, cycle in enumerate(cycles):
            print(f"Cycle {i + 1}: {' -> '.join(cycle[::-1])} -> {cycle[-1]}")
    else:
        print("No contradictory rules present in the above data.")
    