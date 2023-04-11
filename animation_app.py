import os
import time
import webbrowser
import pyautogui

import openai
from utils.parser import ArgumentParser
from utils.opts import animation_opts
 
def find_parens(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '{':
            pstack.append(i)
        elif c == '}':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


def animator(theme, creative):
    """
    Prompts the Completion API to figure out whether the input provided is inappropriate for a generative ai product.
    The prompt has been tested with both english and hindi (roman script) offensive content (slangs, and other offensive slurs).
    Even with unorthodox spellings, the Completion API was reliably able to flag content such that I didn't note any failure modes.
    """
    # -- Prompt for content moderation -> tested on playground
    if creative:
        prompt = f'Write a script in the p5.js framework acting as a seasoned generative art programmer. The animation should be loop infinitely, be highly abstract, extremely bold, exhibit an unprecedented geometric space. Assume a canvas size of 400x400. Do not write code for the setup() function. The theme of the animation is "{theme}".\nConsider using unorthodox polygons, noise, evolving fractals.\nDo not include anything other than the code itself in your response. Do not add any comments.'
    else:
        prompt = f'Write a script in the p5.js framework acting as a seasoned generative art programmer. The animation should be loop infinitely, be highly abstract, extremely bold, exhibit an unprecedented geometric space. Assume a canvas size of 400x400. Do not write code for the setup() function. The theme of the animation is "{theme}".\nDo not include anything other than the code itself in your response. Do not add any comments.'

    # -- Temperature was set to 0.0 to get only the most obvious outputs, no creativity
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        n=1,
        max_tokens=500,
    )

    # -- Return generated command
    return completion.choices[0].message.content

def setup_fn(file):
    setup_template = """
function setup() {
    createCanvas(400, 400);
}
"""
    file.write(setup_template)

def format_draw(draw_fn, duration):
    split = draw_fn.split("function draw() {\n")
    draw_capt_template = """
function draw() {
    if (frameCount === 1) {
        capturer.start()
    }
"""
    func = split[0] + draw_capt_template + split[1]
    before_context = len(split[0])

    settings = {"duration": duration}

    capturer_template = """
    if (frameCount < 60 * {duration}) {{
        capturer.capture(canvas)
    }} else if (frameCount === 60 * {duration}) {{
        capturer.save()
        capturer.stop()
    }}
"""
    start_index = before_context + 17 # -- Index of starting bracket
    end_index = find_parens(func)
    end_index = end_index.get(start_index) - 1

    formatted_func = func[:end_index-1] + capturer_template.format(**settings) + func[end_index-1:]
    return formatted_func

def populate_script(draw_fn, duration):
    with open("./lib/empty-example/sketch.js", "w") as file:
        setup_fn(file)
        file.write(format_draw(draw_fn, duration))


def _get_parser():
    parser = ArgumentParser(description="app.py")
    animation_opts(parser)
    return parser


def main():
    openai.api_key = os.environ["API_KEY"]

    # -- Initialize parser
    parser = _get_parser()
    args = parser.parse_args()

    draw_fn = animator(args.theme, args.added_creativity)
    populate_script(draw_fn, args.duration)

    # -- Open html page to convert animation to webm
    filename = "./lib/empty-example/index.html"
    webbrowser.open_new_tab(filename)

    # -- Close webpage after a couple of minutes
    time.sleep(120)
    pyautogui.hotkey('ctrl', 'w')

if __name__ == "__main__":
    main()