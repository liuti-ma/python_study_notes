import turtle
import pandas
import numpy
print(pandas.__version__)

screen = turtle.Screen()
screen.title("U.S. States Game")

image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)

data = pandas.read_csv("50_states.csv")



#data = numpy.random.randint(1, 50, size=10)

#df = pandas.DataFrame(data, columns=["random_numbers"])

#print(df)


states_list = data.state.tolist()
count = 0
game_on = True
guessed_states = []

while game_on:
    answer_state = screen.textinput(title=f"{count}/50 Guess the State", prompt="What's another state's name?").title()
    if answer_state == "Exit":
        missing_states = [state for state in  states_list if state not in guessed_states]
        print(missing_states)
        output = pandas.DataFrame(missing_states)
        output.to_csv("states_to_learn.csv")
        break
    if answer_state in states_list:
        count += 1
        writer = turtle.Turtle()
        writer.hideturtle()
        writer.penup()
        state_data = data[data.state == answer_state]
        writer.goto(state_data.x.item(),state_data.y.item())
        writer.pendown()
        writer.write(answer_state)
        guessed_states.append(answer_state)





def get_mouse_click_coor(x,y):
    print(x,y)

turtle.onscreenclick(get_mouse_click_coor)


turtle.mainloop()
#screen.exitonclick()
