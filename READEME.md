# Viral Load Calculator

A desktop application for calculating viral load values for HBV, HCV, and HIV tests. This tool helps medical professionals convert test results and calculate logarithmic values with customizable conversion constants.

## Features

- Calculate viral load values for:
  - Hepatitis B Virus (HBV)
  - Hepatitis C Virus (HCV)
  - Human Immunodeficiency Virus (HIV)
- Convert results to IU/ml
- Calculate logarithmic values
- Customizable conversion constants
- User-friendly interface
- Settings persistence

## Installation

### Windows
1. Download the latest release (`ViralLoadCalculator_Setup.exe`)
2. Run the installer
3. Follow the installation wizard

### From Source
```bash
# Clone the repository
git clone https://github.com/YourUsername/viral-load-calculator.git

# Navigate to the project directory
cd viral-load-calculator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Building from Source

To create your own installer:

1. Install PyInstaller and Inno Setup:
```bash
pip install pyinstaller
```
Download Inno Setup from: https://jrsoftware.org/isdl.php

2. Build the executable:
```bash
pyinstaller viral_load_calculator.spec
```

3. Create the installer using Inno Setup:
- Open Inno Setup Compiler
- Load `viral_load_calculator.iss`
- Click Compile

## Usage

1. Select the viral load type (HBV, HCV, or HIV)
2. Enter the test result
3. Click "Calculate" to see the converted values
4. Use the Settings button to customize conversion constants

## Default Conversion Constants

- HBVL: 0.167
- HCVL: 0.57
- HIVL: 0.59

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Your Name]