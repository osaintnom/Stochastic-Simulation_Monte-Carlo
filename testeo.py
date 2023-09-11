import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from random import randint
from typing import Optional

PRECISION = 100

class Car:
    def __init__(
        self,
        x: float,
        v: float,
        vel_max: float,
        a: float,
        amax: float,
        length: float,
        tr: float,
        vd: float,
        bc: "Car",
        fc: Optional["Car"] = None,
        will_measure: Optional[bool] = False,
        init_frame: Optional[int] = None,
        car_id: Optional[int] = None,
    ):
        """
        Initialize a car object.

        Args:
            x (float): Initial position of the car.
            v (float): Initial velocity of the car (in km/h).
            vel_max (float): Maximum velocity of the car (in km/h).
            a (float): Acceleration of the car (in m/s^2).
            amax (float): Maximum acceleration of the car (in m/s^2).
            length (float): Length of the car (in meters).
            tr (float): Reaction time of the driver (in seconds).
            vd (float): Desired velocity of the car (in km/h).
            bc (Car): Back car (previous car in the queue).
            fc (Car, optional): Front car (next car in the queue). Defaults to None.
            will_measure (bool, optional): Whether the car will measure. Defaults to False.
            init_frame (int, optional): Initial frame for the car. Defaults to None.
            car_id (int, optional): Unique identifier for the car. Defaults to None.
        """
        self.x = x
        self.v = v / 3.6  # Convert velocity to m/s
        self.vel_max = vel_max / 3.6  # Convert velocity to m/s
        self.a = a
        self.amax = amax
        self.length = length
        self.tr = tr
        self.vd = vd / 3.6  # Convert velocity to m/s
        self.b_car = bc
        self.f_car = fc
        self.will_measure = will_measure
        self.init_frame = init_frame
        self.car_id = car_id

        # Initialize other car properties and state
        self.increased_attention = False
        self.decresed_attention = False

    def __str__(self):
        """
        Return a string representation of the car.

        Returns:
            str: String representation of the car.
        """
        return f"Car(x={self.x}, v={self.v * 3.6}, vel_max={self.vel_max * 3.6}, a={self.a}, l={self.length}, tr={self.get_reaction_time()}, vd={self.vd * 3.6}, fc={self.f_car}, bc={self.b_car})"

    def __repr__(self):
        """
        Return a string representation of the car.

        Returns:
            str: String representation of the car.
        """
        return f"Car(x={self.x}, v={self.v * 3.6}, vel_max={self.vel_max * 3.6}, a={self.a}, l={self.length}, tr={self.get_reaction_time()}, vd={self.vd * 3.6}, fc={self.f_car}, bc={self.b_car})"

    def check_crash(self):
        """
        Check if the car has crashed with the front car and update its status.
        """
        if self.f_car and self.collides():
            # Update car status due to crash
            pass

    def check_rear_end(self):
        """
        Check if the car has been rear-ended and update its status.
        """
        if self.b_car and self.b_car.collides():
            # Update car status due to rear-end collision
            pass

    def accelerate(self):
        """
        Accelerate the car.
        """
        if self.v < self.vel_max:
            self.v = min(self.v + self.a, self.vel_max)

    def decelerate(self):
        """
        Decelerate the car.
        """
        if self.v > 0:
            self.v = max(self.v - self.a, 0)

    def stop(self):
        """
        Stop the car.
        """
        self.v = 0

    def keep_velocity(self):
        """
        Keep the current velocity of the car.
        """
        pass

    def distance_to_front_car(self) -> Optional[float]:
        """
        Calculate the distance to the front car.

        Returns:
            float: Distance to the front car (front car's position - car's position).
        """
        if self.f_car:
            return self.f_car.x - self.x
        else:
            return None

    def distance_to_back_car(self) -> Optional[float]:
        """
        Calculate the distance to the back car.

        Returns:
            float: Distance to the back car (car's position - back car's position).
        """
        if self.b_car:
            return self.x - self.b_car.x
        else:
            return None

    def get_position(self):
        """
        Get the current position of the car.

        Returns:
            float: Current position of the car.
        """
        return self.x

    def dead_stop(self):
        """
        Bring the car to a complete stop.
        """
        self.v = 0

    def set_initial_frame(self, frame: int):
        """
        Set the initial frame for the car.

        Args:
            frame (int): Initial frame number.
        """
        self.init_frame = frame

    def get_initial_frame(self):
        """
        Get the initial frame for the car.

        Returns:
            int: Initial frame number.
        """
        return self.init_frame

    def set_highway(self, highway):
        """
        Set the highway reference for the car.

        Args:
            highway: Reference to the highway object.
        """
        self.highway = highway

    def update(self, frame: int):
        """
        Update the car's state for the given frame.

        Args:
            frame (int): Current frame number.
        """
        self.resolve_actions(frame)
        self.behaviour(frame)
        # Update car state based on frame

    def resolve_actions(self, frame):
        """
        Resolves actions in the action queue for the car.

        Args:
            frame (int): The current frame of the simulation.

        Returns:
            None
        """
        for action, action_frame in self.action_queue:
            if frame <= action_frame:
                p = np.random.uniform()
                if p < 0.1:
                    for _ in range(100):
                        action()
                if p < 0.07:
                    action()

        # Remove actions that have been taken
        self.action_queue = [
            action_pair for action_pair in self.action_queue if action_pair[1] >= frame
        ]

    def increase_attention(self):
        """
        Increases the driver's attention level.

        Returns:
            None
        """
        self.increased_attention = True

    def default_attention(self):
        """
        Resets the driver's attention level to the default value.

        Returns:
            None
        """
        self.increased_attention = False

    def get_reaction_time(self):
        """
        Get the driver's reaction time based on their attention level.

        Returns:
            float: The driver's reaction time in seconds.
        """
        if self.increased_attention:
            return self.tr / 2
        elif self.decresed_attention:
            return self.tr * 1.5
        return self.tr

    def crashes_upfront(self):
        """
        Checks if there are crashes happening in front of the car.

        Returns:
            bool: True if there are crashes upfront, False otherwise.
        """
        if self.highway:
            for car in self.highway.get_cars():
                if car.x > self.x and car.collides():
                    return True
        return False

    def custom_behavior(self):
        """
        Defines the car's custom behavior.

        Returns:
            None
        """
        if self.x > 8000 and self.x < 9000 and np.random.poisson(10) == 1:
            self.v = 10000

    def behaviour(self, frame):
        """
        Defines the car's behavior based on the current frame and surrounding conditions.

        Args:
            frame (int): The current frame of the simulation.

        Returns:
            None
        """
        if self.crashes_upfront():
            if not self.increased_attention:
                self.action_queue.append((self.increase_attention, frame + 1))

            if self.v > 0:
                self.action_queue.append(
                    (self.decelerate, frame + self.get_reaction_time())
                )
        else:
            if self.increased_attention:
                self.action_queue.append((self.default_attention, frame + 1))

        if self.f_car is not None and self.f_car.a < 0 and self.v > 0:
            self.action_queue.append(
                (self.decelerate, frame + self.get_reaction_time())
            )

        if self.f_car is not None:
            if self.v < self.desired_velocity:
                if self.f_car.has_collided():
                    self.action_queue.append(
                        (self.stop, frame + self.get_reaction_time())
                    )

                    self.action_queue.append(
                        (self.decelerate, frame + self.get_reaction_time())
                    )
                elif self.distance_to_front_car() <= 5 * self.v:
                    self.action_queue.append(
                        (self.decelerate, frame + self.get_reaction_time())
                    )
                elif self.v < self.f_car.v:
                    self.action_queue.append(
                        (self.accelerate, frame + self.get_reaction_time())
                    )
            else:
                if self.f_car.has_collided():
                    if self.distance_to_front_car() <= self.a / 2:
                        self.action_queue.append(
                            (self.decelerate, frame + self.get_reaction_time())
                        )
                    else:
                        self.action_queue.append(
                            (self.keep_velocity, frame + self.get_reaction_time())
                        )

                elif self.distance_to_front_car() <= 5 * self.v:
                    self.action_queue.append(
                        (self.decelerate, frame + self.get_reaction_time())
                    )
        else:
            if self.v < self.desired_velocity:
                self.action_queue.append(
                    (self.accelerate, frame + self.get_reaction_time())
                )

    def collides(self):
        """
        Checks if the car has collided with another car.

        Returns:
            bool: True if the car has collided, False otherwise.
        """
        # Implement collision logic
        pass

    def has_collided(self):
        """
        Checks if the car has been involved in a collision.

        Returns:
            bool: True if the car has been involved in a collision, False otherwise.
        """
        # Implement collision logic
        pass


class Highway:
    def __init__(self, length: float):
        """
        Initialize a highway object.

        Args:
            length (float): Length of the highway (in meters).
        """
        self.length = length
        self.cars = []
        self.time = 0
        self.crashes = []
        self.crash_remove_delay = 5000
        self.historic_ids = []

    def __str__(self):
        """
        Return a string representation of the highway.

        Returns:
            str: String representation of the highway.
        """
        return (
            f"Highway(length={self.length}, cars=[\n"
            + "\n".join([f"\t{car}" for car in self.cars])
            + "\n])"
        )

    def __repr__(self):
        """
        Return a string representation of the highway.

        Returns:
            str: String representation of the highway.
        """
        return (
            f"Highway(length={self.length}, cars=[\n"
            + "\n".join([f"\t{car}" for car in self.cars])
            + "\n])"
        )

    def get_front_car(self):
        """
        Get the front car on the highway.

        Returns:
            Car or None: The front car or None if there are no cars.
        """
        if len(self.cars) == 0:
            return None
        return self.cars[-1]

    def get_back_car(self):
        """
        Get the back car on the highway.

        Returns:
            Car or None: The back car or None if there are no cars.
        """
        if len(self.cars) == 0:
            return None
        return self.cars[0]

    def add_car(self, car: Car):
        """
        Add a car to the highway.

        Args:
            car (Car): The car to be added to the highway.
        """
        if not car.id:
            car.id = len(self.historic_ids)
            self.historic_ids.append(car.id)
        if car.id and car.id not in self.historic_ids:
            self.historic_ids.append(car.id)

        if car.get_position() is None:
            car.x = 0
            self.cars = [car] + self.cars

            if len(self.cars) > 1:
                self.cars[1].b_car = car
                self.cars[0].f_car = self.cars[1]
            return

        if car.get_position() == 0:
            if len(self.cars) > 0:
                self.cars[0].b_car = car
                car.f_car = self.cars[0]
            self.cars = [car] + self.cars
            return

        if car.get_position() > self.length:
            # raise ValueError("Car position is greater than highway length")
            return

        if len(self.cars) > 0:
            car.b_car = self.cars[-1]
            self.cars[-1].f_car = car

        self.cars.append(car)

        car.set_highway(self)

    def remove_car(self, car: Car):
        """
        Remove a car from the highway.

        Args:
            car (Car): The car to be removed from the highway.
        """
        if car in self.cars:
            print(f"AGP: Removing car {car.id} from highway at frame {self.time}")
            # Remove references to car
            if car.f_car:
                car.f_car.b_car = car.b_car
            if car.b_car:
                car.b_car.f_car = car.f_car

            self.cars.remove(car)

    def tow_cars(self, now: bool = False):
        """
        Tow crashed cars from the highway.

        Args:
            now (bool, optional): If True, remove crashed cars immediately. Defaults to False.
        """
        for car, frame in self.crashes:
            if now or frame + self.crash_remove_delay == self.time:
                self.remove_car(car)
                self.crashes.remove((car, frame))

    def update(self, frame: int):
        """
        Update the state of the highway and cars for the given frame.

        Args:
            frame (int): Current frame number.
        """
        for car in self.cars:
            car.update(frame)

            if car.crashed:
                if car not in [c for c, _ in self.crashes]:
                    print(f"AGP: Car {car.id} crashed at frame {frame}, queueing tow")
                    self.crashes.append((car, frame))

            if self.has_crashes():
                self.tow_cars()

            if car.get_position() > self.length:
                self.cars.remove(car)

            if len(self.cars) > 0:
                self.cars[-1].f_car = None

        if len(self.cars) == 0:
            return 2

        self.time += 1

        return 1

    def has_crashes(self) -> bool:
        """
        Check if there are crashed cars on the highway.

        Returns:
            bool: True if there are crashed cars, False otherwise.
        """
        return len(self.crashes) > 0

    def run(self, time: float):
        """
        Run the highway simulation for a specified duration.

        Args:
            time (float): Duration of the simulation (in seconds).
        """
        pass

    def measure(self):
        """
        Measure various statistics and properties of the highway and cars.
        """
        pass

    def plot(self):
        """
        Plot the current state of the highway and cars.
        """
        pass

    def get_cars_positions(self):
        """
        Get the positions of cars on the highway.

        Returns:
            List[float]: List of car positions.
        """
        positions = [car.get_position() for car in self.cars]
        return positions

    def get_cars_velocities(self):
        """
        Get the velocities of cars on the highway.

        Returns:
            List[float]: List of car velocities.
        """
        velocities = [car.v for car in self.cars]
        return velocities

    def get_cars_accelerations(self):
        """
        Get the accelerations of cars on the highway.

        Returns:
            List[float]: List of car accelerations.
        """
        accelerations = [car.a for car in self.cars]
        return accelerations

    def get_cars_times(self):
        """
        Get the elapsed times of cars on the highway.

        Returns:
            List[int]: List of elapsed times for cars.
        """
        times = [car.t for car in self.cars]
        return times

    def get_cars_reaction_times(self):
        """
        Get the reaction times of cars on the highway.

        Returns:
            List[float]: List of car reaction times.
        """
        reaction_times = [car.get_reaction_time() for car in self.cars]
        return reaction_times

    def get_cars_desired_velocities(self):
        """
        Get the desired velocities of cars on the highway.

        Returns:
            List[float]: List of car desired velocities.
        """
        desired_velocities = [car.desired_velocity for car in self.cars]
        return desired_velocities

    def get_cars_front_cars(self):
        """
        Get the front cars of cars on the highway.

        Returns:
            List[Car]: List of front cars for cars.
        """
        front_cars = [car.f_car for car in self.cars]
        return front_cars

    def get_cars_back_cars(self):
        """
        Get the back cars of cars on the highway.

        Returns:
            List[Car]: List of back cars for cars.
        """
        back_cars = [car.b_car for car in self.cars]
        return back_cars


if __name__ == "__main__":
    highway_length = 2000  # Length of the highway in meters
    simulation_time = 100  # Simulation time in time steps

    highway = Highway(highway_length)

    for i in range(20):
        # Set initial position to -1 for the first car, and stagger the rest by 0.2 meters
        initial_position = -1 if i == 0 else -1 + i * 0.2
        car = Car(
            x=initial_position,
            v=randint(0, 120),  # Random initial velocity in km/h
            vel_max=120,  # Maximum velocity in km/h (corrected variable name)
            a=2,  # Acceleration in m/s^2
            amax=3,  # Maximum acceleration in m/s^2 (you can adjust this value)
            length=5,  # Car length in meters
            tr=1.0,  # Reaction time in seconds
            vd=randint(60, 120),  # Random desired velocity in km/h
            bc=None,
            fc=None,
            will_measure=False,
        )
        highway.add_car(car)

    highway.run(simulation_time)



    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
