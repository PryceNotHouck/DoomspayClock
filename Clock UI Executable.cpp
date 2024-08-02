// Used here: Winbase.h header documentation and WinAPI documentation directory from Microsoft, various feature-sepcific
// implementation questions on Stack Overflow, Windows App Development guide, GeeksForGeeks guide to CSV management in
// C++, Microsoft guide to errors and exception handling in C++.

#include <windows.h>
#include <cmath>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <map>
#include <set>
using namespace std;

// global variables
HINSTANCE hInst;
LPCSTR szTitle = "Circle Window"; // window title
LPCSTR szWindowClass = "CIRCLEWINDOW"; // window class name

// forward declarations of functions included in this code module:
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// global variables for clock hands and time input
static string timeInput = "12:00";
static string currYear;
static int hour = 0, minute = 0, second = 0;
map<string, vector<int>> highlights;
static vector<string> variables;
static bool isDepression = false;
static bool drawHighlights = false;
static HWND timeRemainingText;

// control IDs
#define ID_COMBOBOX 101
#define ID_SUBMIT 102
#define ID_TEXT 103

// entry point here
int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // register window class
    WNDCLASSEX wcex;
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(nullptr, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = nullptr;
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = LoadIcon(nullptr, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex)) {
        MessageBox(nullptr, "Call to RegisterClassEx failed!", "Win32 Guided Tour", MB_OK);
        return 1;
    }

    // create the window
    HWND hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 500, 500,
                             nullptr, nullptr, hInstance, nullptr);

    if (!hWnd) {
        MessageBox(nullptr, "Call to CreateWindow failed!", "Win32 Guided Tour", MB_OK);
        return 1;
    }

    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);

    //main message loop
    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return (int)msg.wParam;
}

void getHighlights(const string& filepath, const string& year) {
    drawHighlights = true;
    ifstream file;
    multiset<pair<float, int>> values;
    string row;
    string temp;

    file.open(filepath);
    getline(file, row);
    stringstream vars(row);
    while (getline(vars, temp, ',')) {
        variables.push_back(temp);
    }

    getline(file, row);
    stringstream vals(row);
    int i = -1;
    while (getline(vals, temp, ',')) {
        i++;
        values.insert({abs(stof(temp)), i});
    }

    auto iter = values.end();
    for (int j = 0; j < 3; j++) {
        iter--;
        pair<float, int> fromEnd = *iter;
        highlights[year].push_back(fromEnd.second);
    }
}

float CrisisScore(const string& year) {
    float score = 0.00000000;
    string filepath = R"(..\Get Data\Normalized Years\)" + year + "_normalized.csv";
    ifstream file;
    file.open(filepath);
    if (!file.is_open()) {
        cout << "Could not open " << filepath << endl;
        throw invalid_argument("Normalized annual data for given year not found.");
    }
    getHighlights(filepath, year);

    vector<string> entries;
    string entry;
    string row;
    string check;
    getline(file, row);
    getline(file, row);
    stringstream s(row);
    while (getline(s, entry, ',')) {
        entries.push_back(entry);
    }

    for (const auto& e : entries) {
        score += stof(e);
    }
    score = abs(score);
    return abs(logf(score));
}

void ParseTimeInput(const string& input) {
    float noon = CrisisScore("1955");
    float midnight = CrisisScore("2009");
    float current = CrisisScore(input);

    // Due to the unique nature of the economic struggle faced during the great depression with variables difficult to
    // compare to any other time period, 1929 - 1940 have a unique +10 crisis score penalty to keep the final time in
    // line with other years.
    if (stoi(input) >= 1929 && stoi(input) <= 1940)
        current += 10;
    float ttm = ((2 * (current - midnight))/(noon - midnight)) - 1;
    float time = (ttm * 21600) + 21600;

    if (stoi(input) <= 1940) {
        isDepression = true;
        int hours = 0;
        int minutes = 0;
        int seconds = 0;
        while (time + 3600 <= 0) {
            hours++;
            time += 3600;
        }
        while (time + 60 <= 0) {
            minutes++;
            time += 60;
        }
        while (time + 1 <= 0) {
            seconds++;
            time++;
        }
        hour = hours;
        minute = minutes;
        second = seconds;
    } else {
        isDepression = false;
        int hours = 0;
        int minutes = 0;
        int seconds = 0;
        while (time - 3600 >= 0) {
            hours++;
            time -= 3600;
        }
        while (time - 60 >= 0) {
            minutes++;
            time -= 60;
        }
        while (time - 1 >= 0) {
            seconds++;
            time--;
        }
        hour = hours;
        minute = minutes;
        second = seconds;
    }
}

// function to draw the clock hands
void DrawClockHands(HDC hdc, int centerX, int centerY, int radius) {
    // calculate hand positions
    double hourAngle;
    double minuteAngle;
    double secondAngle;
    if (isDepression) {
        hourAngle = 0;
        minuteAngle = 0;
        secondAngle = 0;
    } else {
        hourAngle = ((hour % 12 + minute / 60.0) * 2 * 3.14159 / 12) * -1;
        minuteAngle = (minute * 2 * 3.14159 / 60) * -1;
        secondAngle = (second * 2 * 3.14159 / 60) * -1;
    }

    int hourHandLength = radius * 0.5;
    int minuteHandLength = radius * 0.75;
    int secondHandLength = radius;

    // hour hand start
    int hourHandX = centerX + (int)(hourHandLength * sin(hourAngle));
    int hourHandY = centerY - (int)(hourHandLength * cos(hourAngle));

    // minute hand start
    int minuteHandX = centerX + (int)(minuteHandLength * sin(minuteAngle));
    int minuteHandY = centerY - (int)(minuteHandLength * cos(minuteAngle));
    
    // second hand start
    int secondHandX = centerX + (int)(secondHandLength * sin(secondAngle));
    int secondHandY = centerY - (int)(secondHandLength * cos(secondAngle));

    // draw hour hand
    HPEN drawHour = CreatePen(PS_SOLID, 4, RGB(255, 0, 0)); // Red color for hour hand
    HPEN oldDrawHour = (HPEN)SelectObject(hdc, drawHour);
    MoveToEx(hdc, centerX, centerY, nullptr);
    LineTo(hdc, hourHandX, hourHandY);
    SelectObject(hdc, oldDrawHour);
    DeleteObject(drawHour);

    // draw minute hand
    HPEN drawMinute = CreatePen(PS_SOLID, 3, RGB(0, 0, 255)); // Blue color for minute hand
    HPEN oldDrawMinute = (HPEN)SelectObject(hdc, drawMinute);
    MoveToEx(hdc, centerX, centerY, nullptr);
    LineTo(hdc, minuteHandX, minuteHandY);
    SelectObject(hdc, oldDrawMinute);
    DeleteObject(drawMinute);
    
    // draw second hand
    HPEN drawSecond = CreatePen(PS_SOLID, 2, RGB(0, 255, 0)); // Green color for second hand
    HPEN oldDrawSecond = (HPEN) SelectObject(hdc, drawSecond);
    MoveToEx(hdc, centerX, centerY, nullptr);
    LineTo(hdc, secondHandX, secondHandY);
    SelectObject(hdc, oldDrawSecond);
    DeleteObject(drawSecond);
}

// function to update the text box with remaining minutes until midnight
void UpdateRemainingTime() {
    stringstream ss;
    if (isDepression) {
        ss << "Great Depression Year, " << hour << " hours, " << minute << " minutes, and " << second << " seconds past midnight.";
    } else {
        ss << hour << " hours, " << minute << " minutes, and " << second << " seconds to midnight.";
    }
    SetWindowText(timeRemainingText, ss.str().c_str());
}

string addFlavorText(string text, int i) {
    if (text == "GDP Delta") {
        if (i == 1) {
            text = "Negative GDP Growth\nThis year's most damaging feature\nis its major decline in annual GDP.";
        } else if (i == 2) {
            text = "Negative GDP Growth\nThis year's second most damaging feature\nis its moderate decline in annual GDP.";
        } else {
            text = "Negative GDP Growth\nThis year's third most damaging feature\nis its notable decline in annual GDP.";
        }
    } else if (text == "Average Unemployment\r") {
        if (i == 1) {
            text = "Unemployment\nThis year's most damaging feature\nis its substantial increase in unemployment.";
        } else if (i == 2) {
            text = "Unemployment\nThis year's second most damaging feature\nis its moderate increase in unemployment.";
        } else {
            text = "Unemployment\nThis year's third most damaging feature\nis its notable increase in unemployment.";
        }
    } else if (text == "Average Labor Force") {
        if (i == 1) {
            text = "Labor Availability\nThis year's most damaging feature is\nits major drop in the availability of workers.";
        } else if (i == 2) {
            text = "Labor Availability\nThis year's second most damaging feature is\nits moderate drop in the availability of workers.";
        } else {
            text = "Labor Availability\nThis year's third most damaging feature is\nits notable drop in the availability of workers.";
        }
    } else if (text == "Personal Savings %") {
        if (i == 1) {
            text = "Low Personal Savings\nThis year's most damaging feature is its\nsignificant shortage in personal savings.";
        } else if (i == 2) {
            text = "Low Personal Savings\nThis year's second most damaging feature\nis it moderate shortage in personal savings.";;
        } else {
            text = "Low Personal Savings\nThis year's third most damaging feature\nis its notable shortage in personal savings.";;
        }
    } else if (text == "Goods Consumption") {
        if (i == 1) {
            text = "Goods Consumption\nThis year's most damaging features is its\nmajor decline in the\nconsumption of consumer goods.";
        } else if (i == 2) {
            text = "Goods Consumption\nThis year's second most damaging features\nis its moderate decline in\nthe consumption of consumer goods.";
        } else {
            text = "Goods Consumption\nThis year's third most damaging features\n is its notable decline in\nthe consumption of consumer goods.";
        }
    } else if (text == "Government Consumption and Gross Investment") {
        if (i == 1) {
            text = "Government Spending\nThis year's most damaging feature is its\nirresponsible government\nconsumption and investment.";
        } else if (i == 2) {
            text = "Government Spending\nThis year's second most damaging feature\nis its irresponsible government\nconsumption and investment.";
        } else {
            text = "Government Spending\nThis year's third most damaging feature\nis its irresponsible government\nconsumption and investment.";
        }
    } else if (text == "Import of Goods") {
        if (i == 1) {
            text = "Import of Goods\nThis year's most damaging feature is its\nmajor decline in the import\nof foreign goods.";
        } else if (i == 2) {
            text = "Import of Goods\nThis year's second most damaging feature\nis its moderate decline in the import\nof foreign goods.";
        } else {
            text = "Import of Goods\nThis year's third most damaging feature\nis its notable decline in the import\nof foreign goods.";
        }
    } else if (text == "Average Interest Rate") {
        if (i == 1) {
            text = "High Interest Rates\nThis year's most damaging feature is its\nincredibly high interest rates.";
        } else if (i == 2) {
            text = "High Interest Rates\nThis year's second most damaging feature\nis its moderately high interest rates.";
        } else {
            text = "High Interest Rates\nThis year's third most damaging feature\nis its notably high interest rates.";
        }
    } else if (text == "Average Inflation Rate") {
        if (i == 1) {
            text = "High Inflation\nThis year's most damaging feature is its\nvery high rate of inflation.";
        } else if (i == 2) {
            text = "High Inflation\nThis year's second most damaging feature\nis its moderately high rate of inflation.";
        } else {
            text = "High Inflation\nThis year's third most damaging feature\nis its notably high rate of inflation.";
        }
    } else if (text == "Residential") {
        if (i == 1) {
            text = "Housing Availability\nThis year's most damaging feature is its\nremarkably low access to housing.";
        } else if (i == 2) {
            text = "Housing Availability\nThis year's second most damaging feature\nis its moderately low access to housing.";
        } else {
            text = "Housing Availability\nThis year's third most damaging feature\nis its notably low access to housing.";
        }
    } else if (text == "Average All Loans Default Rate") {
        if (i == 1) {
            text = "Default Rate - All Loans\nThis year's most damaging feature is its\nincredibly high default rate on all loans.";
        } else if (i == 2) {
            text = "Default Rate - All Loans\nThis year's second most damaging feature\nis its moderately high default rate on all loans.";
        } else {
            text = "Default Rate - All Loans\nThis year's third most damaging feature\nis its notably high default rate on all loans.";
        }
    } else if (text == "Consumer Confidence") {
        if (i == 1) {
            text = "Consumer Confidence\nThis year's most damaging feature is its\nvery low consumer confidence index.";
        } else if (i == 2) {
            text = "Consumer Confidence\nThis year's second most damaging feature\nis its moderately low consumer confidence index.";
        } else {
            text = "Consumer Confidence\nThis year's third most damaging feature\nis its notably low consumer confidence index.";
        }
    } else if (text == "Average Median Price") {
        if (i == 1) {
            text = "Housing Market\nThis year's most damaging feature is its\nseverely prohibitive housing market.";
        } else if (i == 2) {
            text = "Housing Market\nThis year's second most damaging feature is its\nmoderately prohibitive housing market.";
        } else {
            text = "Housing Market\nThis year's third most damaging feature is its\nnotably prohibitive housing market.";
        }
    } else if (text == "Year-In Change") {
        if (i == 1) {
            text = "Housing Price Change\nThis year's most damaging feature is its\nsevere change in housing prices.";
        } else if (i == 2) {
            text = "Housing Price Change\nThis year's second most damaging feature\nis its moderate change in housing prices.";
        } else {
            text = "Housing Price Change\nThis year's third most damaging feature\nis its notable change in housing prices.";
        }
    }
    return text;
}

void drawHighlight(HDC hdc, int top, int bottom, int left, int right, HBRUSH color, string text, int box) {
    text = addFlavorText(text, box);
    RECT highlight_box = {left, top, right, bottom};
    HPEN drawOutline = CreatePen(PS_SOLID, 3, RGB(0, 0, 0));
    auto oldBrush = (HBRUSH)SelectObject(hdc, color);
    auto oldDrawOutline = (HPEN)SelectObject(hdc, drawOutline);

    FillRect(hdc, &highlight_box, color);
    Rectangle(hdc, left, top, right, bottom);
    SelectObject(hdc, oldDrawOutline);
    DeleteObject(drawOutline);
    SetBkMode(hdc, TRANSPARENT);

    SetTextColor(hdc, RGB(0, 0, 0));
    LPCSTR box_text = text.c_str();

    DrawText(hdc, box_text, -1, &highlight_box, DT_CENTER | DT_VCENTER);
    SelectObject(hdc, oldBrush);
}

// window procedure function
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    static HBRUSH black;
    static HBRUSH white;
    static HBRUSH grey;
    static HBRUSH red;
    static HBRUSH orange;
    static HBRUSH yellow;
    static HWND years;
    static HWND submit;
    static HWND highlight1;
    static HWND highlight2;
    static HWND highlight3;

    switch (message) {
        case WM_CREATE:
            // create brushes for black and white
            black = CreateSolidBrush(RGB(0, 0, 0));
            white = CreateSolidBrush(RGB(255, 255, 255));
            grey = CreateSolidBrush(RGB(196, 196, 196));
            red = CreateSolidBrush(RGB(195, 40, 23));
            orange = CreateSolidBrush(RGB(195, 126, 23));
            yellow = CreateSolidBrush(RGB(178, 195, 23));

            // create a combobox for year selection
            years = CreateWindow("COMBOBOX", nullptr, WS_CHILD | WS_VSCROLL | WS_VISIBLE | CBS_DROPDOWNLIST,
                                     50, 50, 100, 500, hWnd, (HMENU)ID_COMBOBOX,
                                     GetModuleHandle(nullptr), nullptr);

            // populate combobox with years from 1930 to 2024
            for (int i = 1929; i <= 2023; i++) {
                stringstream ss;
                ss << i;
                SendMessage(years, CB_ADDSTRING, 0, (LPARAM)ss.str().c_str());
            }

            // set default selection
            SendMessage(years, CB_SETCURSEL, 0, 0);

            // create a button to submit the selected year
            submit = CreateWindow("BUTTON", "Set Time", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 160, 50, 75, 25, hWnd,
                                  (HMENU)ID_SUBMIT, GetModuleHandle(nullptr), nullptr);

            // create a static text control for displaying remaining minutes
            timeRemainingText = CreateWindow("STATIC", "", WS_CHILD | WS_VISIBLE, 50, 90, 250, 35, hWnd, (HMENU)ID_TEXT,
                                          GetModuleHandle(nullptr), nullptr);

            UpdateRemainingTime(); // Initialize text
            break;

        case WM_COMMAND:
            if (LOWORD(wParam) == ID_SUBMIT) {
                // get the selected year from the year dropdown
                int index = SendMessage(years, CB_GETCURSEL, 0, 0);
                char buffer[10];
                SendMessage(years, CB_GETLBTEXT, index, (LPARAM)buffer);
                timeInput = buffer;
                currYear = timeInput;
                ParseTimeInput(timeInput);
                InvalidateRect(hWnd, nullptr, TRUE); // Repaint
                UpdateRemainingTime(); // Update remaining time
            }
            break;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);

            // set the background to white
            FillRect(hdc, &ps.rcPaint, grey);

            // draw a white circle with a black border
            RECT rect;
            GetClientRect(hWnd, &rect);
            int centerX = (rect.right - rect.left) / 2;
            int centerY = (rect.bottom - rect.top) / 2;
            int radius = 100; // Radius of the circle

            // create a white brush for the fill and a black pen for the border
            HBRUSH oldBrush = (HBRUSH)SelectObject(hdc, white);
            HPEN blackPen = CreatePen(PS_SOLID, 2, RGB(0, 0, 0));
            HPEN oldPen = (HPEN)SelectObject(hdc, blackPen);

            // draw the filled white circle
            Ellipse(hdc, centerX - radius, centerY - radius, centerX + radius, centerY + radius);

            // draw border of the circle
            SelectObject(hdc, blackPen);
            SelectObject(hdc, oldBrush);
            SelectObject(hdc, oldPen);

            // Cleanup
            DeleteObject(blackPen);

            if (drawHighlights) {
                drawHighlight(hdc, centerY - 170, centerY - 90, centerX + 120, centerX + 420,
                              red, variables[highlights[currYear][0]], 1);
                drawHighlight(hdc, centerY - 70, centerY + 20, centerX + 120, centerX + 420,
                              orange, variables[highlights[currYear][1]], 2);
                drawHighlight(hdc, centerY + 40, centerY + 130, centerX + 120, centerX + 420,
                              yellow, variables[highlights[currYear][2]], 3);
            }

            // draw 60 dashes around circle for minutes
            int dashLength = 10; // length of the normal dashes
            int longDashLength = 15; // length of the thicker 5 dashes
            int thicknessNormal = 1; // thickness of normal dashes
            int thicknessThick = 3; // thickness of thicker dashes

            for (int i = 0; i < 60; ++i) {
                double angle = i * 2 * 3.141592653589793 / 60; // Angle for each dash
                int startX = centerX + (int)((radius - 10) * cos(angle)); // Start point of the dash
                int startY = centerY - (int)((radius - 10) * sin(angle)); // Start point of the dash
                int endX = centerX + (int)((radius - 10 - (i % 5 == 0 ? longDashLength : dashLength)) * cos(angle)); // End point of the dash
                int endY = centerY - (int)((radius - 10 - (i % 5 == 0 ? longDashLength : dashLength)) * sin(angle)); // End point of the dash

                // choose the pen based on dash index
                HPEN hPenDash = CreatePen(PS_SOLID, (i % 5 == 0 ? thicknessThick : thicknessNormal), RGB(0, 0, 0));
                HPEN oldPenDash = (HPEN)SelectObject(hdc, hPenDash);

                // draw dash
                MoveToEx(hdc, startX, startY, nullptr);
                LineTo(hdc, endX, endY);

                SelectObject(hdc, oldPenDash);
                DeleteObject(hPenDash);
            }

            // draw clock hands
            DrawClockHands(hdc, centerX, centerY, radius);

            EndPaint(hWnd, &ps);
        }
            break;

        case WM_DESTROY:
            // clean brushes
            DeleteObject(black);
            DeleteObject(white);
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}
