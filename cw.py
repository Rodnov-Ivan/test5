class Student:
    __slots__ = ['student_id', 'name', 'age', 'specialty']

    def __init__(self, student_id, name, age, specialty):
        """
        Initializes a Student object with the given student ID, name, age, and specialty.
        """
        self.student_id = student_id
        self.name = name
        self.age = age
        self.specialty = specialty

    def update_info(self, name=None, age=None, specialty=None):
        """
        Updates the student's information (name, age, specialty) if the provided arguments are not None.
        """
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if specialty is not None:
            self.specialty = specialty

    def __str__(self):
        """
        Returns a string representation of the Student object, including the student ID, name, age, and specialty.
        """
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Specialty: {self.specialty}"


class HashTable:
    DELETED = "<Deleted>"

    def __init__(self, size=11):
        """
        Initializes a hash table with a given size (default is 11).
        """
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash1(self, student_id):       
        """
        Computes the first hash value based on the student's ID using the golden ratio.
        """
        A = 0.6180339887        
        hash_value = student_id * A
        fractional_part = hash_value - int(hash_value)        
        return int(self.size * fractional_part)

    def _hash2(self, student_id):
        """
        Computes the second hash value for use in double hashing.
        """
        return 1 + (student_id % (self.size - 1))

    def _probe(self, student_id, step):
        """
        Computes the next index for probing during collision resolution using double hashing.
        """
        return (self._hash1(student_id) + step * self._hash2(student_id)) % self.size

    def _resize(self, new_size):
        """
        Resizes the hash table to the given new size and rehashes all existing entries.
        """
        old_table = self.table
        self.size = new_size
        self.table = [None] * self.size
        self.count = 0

        for entry in old_table:
            if entry is not None and entry != self.DELETED:
                self.add(entry)

    def add(self, student):
        """
        Adds a student to the hash table. If the table is more than 70% full, it resizes before adding.
        """
        if self.count / self.size > 0.70: 
            self._resize(self._next_prime(self.size * 2))

        step = 0
        index = self._hash1(student.student_id)

        while self.table[index] is not None and self.table[index] != self.DELETED:
            if self.table[index].student_id == student.student_id:
                self.table[index].update_info(student.name, student.age, student.specialty)
                return
            step += 1
            index = self._probe(student.student_id, step)

        self.table[index] = student
        self.count += 1

    def remove(self, student_id):
        """
        Removes a student from the hash table by student ID. If the table is less than 20% full, it resizes after removal.
        """
        step = 0
        index = self._hash1(student_id)

        while self.table[index] is not None:
            if self.table[index] != self.DELETED and self.table[index].student_id == student_id:
                self.table[index] = self.DELETED
                self.count -= 1
                if self.count / self.size < 0.2: 
                    self._resize(self._next_prime(self.size // 2))
                return True
            step += 1
            index = self._probe(student_id, step)
        return False

    def find(self, student_id):
        """
        Searches for a student by ID and returns their information if found.
        """
        step = 0
        index = self._hash1(student_id)

        while self.table[index] is not None:
            if self.table[index] != self.DELETED and self.table[index].student_id == student_id:
                return str(self.table[index])
            step += 1
            index = self._probe(student_id, step)
        return None

    def list_all(self):
        """
        Returns a string representation of all students in the hash table.
        """
        students = [str(student) for student in self.table if student is not None and student != self.DELETED]
        return "\n".join(students) if students else "No students registered."

    def _next_prime(self, n):
        """
        Finds the next prime number greater than or equal to 'n' for resizing the hash table.
        """
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        while not is_prime(n):
            n += 1
        return n


class RegistrationSystem:
    def __init__(self):
        """
        Initializes the registration system with an empty hash table.
        """
        self.hash_table = HashTable()

    def add_student(self, student_id, name, age, specialty):
        """
        Adds a new student to the registration system and returns a confirmation message.
        """
        student = Student(student_id, name, age, specialty)
        self.hash_table.add(student)
        return f"Student {name} added."

    def remove_student(self, student_id):
        """
        Removes a student from the registration system by student ID and returns a confirmation message.
        """
        if self.hash_table.remove(student_id):
            return f"Student with ID {student_id} removed."
        else:
            return f"No student found with ID {student_id}."

    def update_student(self, student_id, name=None, age=None, specialty=None):
        """
        Updates the information of an existing student by their ID.
        """
        if self.hash_table.find(student_id):
            self.hash_table.add(Student(student_id, name, age, specialty))
            return f"Student with ID {student_id} updated."
        else:
            return f"Student with ID {student_id} not found."

    def find_student(self, student_id):
        """
        Finds and returns the information of a student by their ID.
        """
        student_info = self.hash_table.find(student_id)
        if student_info:
            return student_info
        else:
            return f"No student found with ID {student_id}."

    def list_all_students(self):
        """
        Lists all the students currently registered in the system.
        """
        students = self.hash_table.list_all()
        print(students)
