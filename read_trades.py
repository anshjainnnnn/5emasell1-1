from flask import Flask, render_template_string

app = Flask(__name__)

def read_trades(file_path):
    """
    Reads trades from a text file and splits them by a separator line.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    trades = [trade.strip() for trade in content.split("-------------------------------------------------------------") if trade.strip()]
    return trades

def generate_full_html(trades):
    """
    Generates a complete HTML with inline CSS and JavaScript for a trade slider.
    """
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trade Slider</title>
        <style>
            /* Basic CSS styling for the slider */
            body {{
                font-family: 'Arial', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4; /* Light gray background */
                color: #333; /* Dark text color */
            }}
            .slider {{
                position: relative;
                width: 90%;
                max-width: 800px;
                background-color: #ffffff; /* White slider background */
                padding: 20px;
                border-radius: 10px; /* More rounded corners */
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* Subtle shadow */
                overflow: hidden;
            }}
            .slide {{
                display: none;
                font-size: 1.2em; /* Adjusted font size */
                line-height: 1.5em; /* Improved line spacing */
                color: #000; /* Black text for slide content */
                font-weight: normal; /* Normal text weight */
                transition: opacity 0.5s ease; /* Fade effect */
            }}
            .slide pre {{
                white-space: pre-wrap; /* Wrap long text */
                word-wrap: break-word;
                margin: 0; /* Remove margin for cleaner look */
                padding: 15px; /* Added padding for text */
                border: 1px solid #e0e0e0; /* Light gray border */
                border-radius: 5px; /* Rounded corners for text */
                background-color: #f9f9f9; /* Light background for text box */
                overflow-y: auto; /* Scroll if content is too long */
                max-height: 300px; /* Fixed height for scrollable area */
            }}
            .active {{
                display: block;
                opacity: 1; /* Make current slide visible */
            }}
            .prev, .next {{
                cursor: pointer;
                position: absolute;
                top: 50%;
                width: 40px; /* Fixed width for buttons */
                height: 40px; /* Fixed height for buttons */
                margin-top: -20px; /* Center vertically */
                padding: 0;
                color: #ffffff; /* White button text */
                font-weight: bold;
                font-size: 20px; /* Larger font size for buttons */
                border: none;
                border-radius: 50%;
                background-color: #007bff; /* Blue button background */
                transition: background-color 0.3s, transform 0.3s; /* Smooth transitions */
                display: flex; /* Center icon inside */
                align-items: center; /* Center vertically */
                justify-content: center; /* Center horizontally */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Button shadow */
            }}
            .next {{
                right: 20px; /* Adjust button position */
            }}
            .prev {{
                left: 20px; /* Adjust button position */
            }}
            .prev:hover, .next:hover {{
                background-color: #0056b3; /* Darker blue on hover */
                transform: scale(1.1); /* Slight zoom on hover */
            }}
            .index-input {{
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                padding: 10px;
                font-size: 1em;
                border: 2px solid #007bff; /* Blue border for input */
                border-radius: 5px;
                background-color: #ffffff; /* White background for input */
                color: #333; /* Dark text */
                text-align: center; /* Centered text */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle input shadow */
                width: 150px; /* Fixed width for input */
            }}
            .index-display {{
                position: absolute;
                top: 60px; /* Adjusted for better placement */
                left: 50%;
                transform: translateX(-50%);
                font-size: 1.2em; /* Font size for display */
                color: #333; /* Dark text for current index */
                font-weight: bold; /* Bold text */
            }}
        </style>
    </head>
    <body>
        <div class="slider">
            <input type="number" class="index-input" placeholder="Enter slide number (1-{len(trades)})" min="1" max="{len(trades)}">
            <div class="index-display">1</div>
    '''

    # Add each trade as a slide
    for index, trade in enumerate(trades):
        html_content += f'''
            <div class="slide" data-index="{index}">
                <pre>{trade}</pre>
            </div>
        '''

    # Add the footer with JavaScript
    html_content += '''
        </div>
        <button class="prev">❮</button>
        <button class="next">❯</button>
        <script>
            // JavaScript for handling the slider functionality
            let currentIndex = 0;
            const slides = document.querySelectorAll('.slide');
            const indexDisplay = document.querySelector('.index-display');
            const indexInput = document.querySelector('.index-input');
            
            function showSlide(index) {
                slides.forEach((slide, i) => {
                    slide.style.display = i === index ? 'block' : 'none';
                    slide.style.opacity = i === index ? '1' : '0'; // Fade effect
                });
                indexDisplay.textContent = index + 1; // Display the current slide number
                indexInput.value = index + 1; // Set input value to current index
            }
            
            function nextSlide() {
                currentIndex = (currentIndex + 1) % slides.length;
                showSlide(currentIndex);
            }
            
            function prevSlide() {
                currentIndex = (currentIndex - 1 + slides.length) % slides.length;
                showSlide(currentIndex);
            }
            
            function checkAutoSlide() {
                const currentSlide = slides[currentIndex];
                const slideText = currentSlide.textContent || currentSlide.innerText;
                if (slideText.includes("TRADE END")) {
                    nextSlide();
                }
            }

            indexInput.addEventListener('change', (e) => {
                const value = parseInt(e.target.value) - 1; // Adjusting for 0-based index
                if (value >= 0 && value < slides.length) {
                    currentIndex = value;
                    showSlide(currentIndex);
                } else {
                    indexInput.value = currentIndex + 1; // Reset input if out of range
                }
            });
            
            // Initial display
            showSlide(currentIndex);
            
            // Auto-slide check every 2 seconds
            setInterval(checkAutoSlide, 2000);
            
            // Button controls
            document.querySelector('.prev').addEventListener('click', prevSlide);
            document.querySelector('.next').addEventListener('click', nextSlide);
        </script>
    </body>
    </html>
    '''

    return html_content

@app.route('/')
def index():
    trades = read_trades('MiindBlowing.txt')  # Ensure this file is in the root folder
    html_content = generate_full_html(trades)
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True)
