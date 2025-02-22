// Used here: Winbase.h header documentation and WinAPI documentation directory from Microsoft, various feature-sepcific
// implementation questions on Stack Overflow, Windows App Development guide, GeeksForGeeks guide to CSV management in
// C++, Microsoft guide to errors and exception handling in C++.

//https://learn.microsoft.com/en-us/windows/win32/api/winbase/

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
HINSTANCE inst;
LPCSTR windowTitle = "Circle Window"; // window title
LPCSTR windowClass = "CIRCLEWINDOW"; // window class name

// forward declarations of functions included in this code module:
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// global variables for clock hands and time input
static string timeInput = "12:00";
static string currYear;
static string addInfo1;
static string addInfo2;
static string disclaimerText = "The year selected occurred during the Great\nDepression, an event with causes and\n"
                               "consequences that are difficult to compare to\nany other year in "
                               "American history,\nso take the given time with a grain of salt.";

//if gpd is factor
static string GDPFactor = "\"Negative\" growth represents a decrease in a\ncountry's gross domestic product. Declining "
                          "wage growth\n and a contraction in a country's\nmoney supply are characteristics of such growth,\nand "
                          "economists believe it to be signify a recession/depression.";
static string UnemployFactor = "A high unemployment rate is a potential \ncause for a recession, as"
                               "unemployed \npeople are less likely to spend money\n to stimulate the economy, and more \nlikely to "
                               "cost the government more money\n as they collect financial aid in the form of \nfood stamps etc.";
static string laborForceFactor = "A slowed job market/labor force reflects a \nslowing of the economy, similar to"
                                 "the \nunemployment rate, due to reasons such \nas workers and businesses producing and \n"
                                 "spending less money.";
static string personalSpendFactor = "As the amount of money the people within an economy \ntends to save increases, the "
                                    "total \nrevenues for different companies decreases. \nLess money circulates, causing the economy to \nslow down.";
static string goodsConsumptionFactor = "Consumer spending is the largest portion of where \nthe US' GDP comes from. \nWhen consumers are spending and "
                                       "consuming goods, \nit both spurs economic growth and reflects positively \non economic trends due to the overall ability \nto spend more.";
static string govSpendAndInvestFactor = "Government spending includes the spending on goods and \nservices such as public employee \nsalaries and infrastructure maintenance which can \nincrease the demand for goods. "
                                  "Investments include improving roads, schools, and \nhospitals/research and development. This overall \nincreases the efficiency in the economy over the long run.";
static string importedGoodsFactor = "Imported goods have the potential for positive \neconomic growth, in cases where the imported"
                                    "goods \nimprove efficiency over the long run with machinery \nand equipment at lower prices. The \ndownside is that"
                                    "imported goods also have the \npotential to threaten domestic industries that \ncan not compete with industries abroad.";
static string avgInterestFactor = "When interest rates rise, businesses and consumers cut \nback on spending. This causes earnings and \nstock"
                                "prices to drop.";
static string avgInflationFactor = "Lower inflation rates keep an economy healthy. \nBut when the rate of inflation increases rapidly, purchasing \npower drops. This causes"
                                   "higher interest rates, \nand other negative effects.";
static string residentialFactor = "When housing is less available, and the rate of \nhousing being produced is low, prices become \nunaffordable. When people are unable to afford "
                                  "houses, \nespecially in cities, it limits labor, \nproductivity, and economic growth in general.";
static string allLoanDefaultFactor = "A higher average \"default rate\", specifically \ncompany and housing default rates, shows \nthat the economy is unhealthy because they "
                                     "\ncan not pay off debts owed at all.";
static string consumerConfidenceFactor = "Consumer confidence, when high, means that consumers \nare optimistic and willing to spend more money \nto stimulate the economy. Lower \nCCI can possibly lead to recessions.";
static string medianPriceFactor = "The median price of housing can significantly affect \na consumer's ability to stimulate the economy. \nIf prices are expensive, people need \nto save more and \nsimply pay off mortgages, rather than"
                                  "purchasing \nvarious different goods and services to support \nbusinesses.";
static string yearInChange = "The year-in change of housing prices can strongly \nrepresent causes of a potential economic \ncollapse. As housing prices soar, it can \nillustrate an economy's unwillingness to let go of \nhousing, as well as possible increased"
                             "interest \nrates, higher inflation rates, and other \nnegative economic factors.";
static string yearInBusinessLoanDefaultFactor = "A higher rate/increase in business loan \ndefault rates strongly correlate to a \nfailing economy, "
                                                "due to the perceived increase \nin difficulty for a company to pay off its loans.";






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
int APIENTRY WinMain(HINSTANCE instance, HINSTANCE prevInstance, LPSTR line, int showCommand) {
    // register window class
    WNDCLASSEX wcex;
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = instance;
    wcex.hIcon = LoadIcon(nullptr, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = nullptr;
    wcex.lpszClassName = windowClass;
    wcex.hIconSm = LoadIcon(nullptr, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex)) {
        MessageBox(nullptr, "Call to RegisterClassEx failed!", "Win32 Guided Tour", MB_OK);
        return 1;
    }

    // create the window
    HWND hWnd = CreateWindow(windowClass, windowTitle, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 1200, 800,
                             nullptr, nullptr, instance, nullptr);

    if (!hWnd) {
        MessageBox(nullptr, "Call to CreateWindow failed!", "Win32 Guided Tour", MB_OK);
        return 1;
    }

    ShowWindow(hWnd, showCommand);
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
    else if (stoi(input) >= 2001 && stoi(input) <= 2007)
        current -= 0.25;  // static modifier for CDO-dominated markets, which are also difficult to compare to.
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
    bool hour1 = false;
    if (hour == 1) {
        hour1 = true;
    }
    if (isDepression && hour1) {
        ss << "Great Depression: US was " << hour << " hr, " << minute << " mins, and " << second << " secs past midnight!\n"; //change

    }
    if (!isDepression && hour1) {
        ss << "US in " << currYear << " was " << hour << " hr, " << minute << " mins, and " << second << " secs to midnight...\n";  //change

    }
    if (isDepression) {
        ss << "Great Depression: US was " << hour << " hrs, " << minute << " mins, and " << second << " secs past midnight!\n"; //change
    } else {
        ss << "US in " << currYear << " was " << hour << " hrs, " << minute << " mins, and " << second << " secs to midnight...\n";  //change
    }
    SetWindowText(timeRemainingText, ss.str().c_str());
}

string addFlavorText(string text, int i) {
    if (text == "GDP Delta") {
        if (i == 1) {
            text = "Negative GDP Growth\nThis year's most damaging feature\nis its major decline in annual GDP.";
            addInfo1 = GDPFactor;
        } else if (i == 2) {
            text = "Negative GDP Growth\nThis year's second most damaging feature\nis its moderate decline in annual GDP.";
            addInfo2 = GDPFactor;
        } else {
            text = "Negative GDP Growth\nThis year's third most damaging feature\nis its notable decline in annual GDP.";
        }
    } else if (text == "Average Unemployment\r") {
        if (i == 1) {
            text = "Unemployment\nThis year's most damaging feature\nis its substantial increase in unemployment.";
            addInfo1 = UnemployFactor;
        } else if (i == 2) {
            text = "Unemployment\nThis year's second most damaging feature\nis its moderate increase in unemployment.";
            addInfo2 = UnemployFactor;
        } else {
            text = "Unemployment\nThis year's third most damaging feature\nis its notable increase in unemployment.";
        }
    } else if (text == "Average Labor Force") {
        if (i == 1) {
            text = "Labor Availability\nThis year's most damaging feature is\nits major drop in the availability of workers.";
            addInfo1 = laborForceFactor;

        } else if (i == 2) {
            text = "Labor Availability\nThis year's second most damaging feature is\nits moderate drop in the availability of workers.";
            addInfo2 = laborForceFactor;

        } else {
            text = "Labor Availability\nThis year's third most damaging feature is\nits notable drop in the availability of workers.";
        }
    } else if (text == "Personal Savings %") {
        if (i == 1) {
            text = "Low Personal Savings\nThis year's most damaging feature is its\nsignificant shortage in personal savings.";
            addInfo1 = personalSpendFactor;

        } else if (i == 2) {
            text = "Low Personal Savings\nThis year's second most damaging feature\nis it moderate shortage in personal savings.";
            addInfo2 = personalSpendFactor;

        } else {
            text = "Low Personal Savings\nThis year's third most damaging feature\nis its notable shortage in personal savings.";
        }
    } else if (text == "Goods Consumption") {
        if (i == 1) {
            text = "Goods Consumption\nThis year's most damaging features is its\nmajor decline in the\nconsumption of consumer goods.";
            addInfo1 = goodsConsumptionFactor;

        } else if (i == 2) {
            text = "Goods Consumption\nThis year's second most damaging features\nis its moderate decline in\nthe consumption of consumer goods.";
            addInfo2 = goodsConsumptionFactor;

        } else {
            text = "Goods Consumption\nThis year's third most damaging features\n is its notable decline in\nthe consumption of consumer goods.";
        }
    } else if (text == "Government Consumption and Gross Investment") {
        if (i == 1) {
            text = "Government Spending\nThis year's most damaging feature is its\nirresponsible government\nconsumption and investment.";
            addInfo1 = govSpendAndInvestFactor;

        } else if (i == 2) {
            text = "Government Spending\nThis year's second most damaging feature\nis its irresponsible government\nconsumption and investment.";
            addInfo2 = govSpendAndInvestFactor;

        } else {
            text = "Government Spending\nThis year's third most damaging feature\nis its irresponsible government\nconsumption and investment.";
        }
    } else if (text == "Import of Goods") {
        if (i == 1) {
            text = "Import of Goods\nThis year's most damaging feature is its\nmajor decline in the import\nof foreign goods.";
            addInfo1 = importedGoodsFactor;

        } else if (i == 2) {
            text = "Import of Goods\nThis year's second most damaging feature\nis its moderate decline in the import\nof foreign goods.";
            addInfo2 = importedGoodsFactor;

        } else {
            text = "Import of Goods\nThis year's third most damaging feature\nis its notable decline in the import\nof foreign goods.";
        }
    } else if (text == "Average Interest Rate") {
        if (i == 1) {
            text = "High Interest Rates\nThis year's most damaging feature is its\nincredibly high interest rates.";
            addInfo1 = avgInterestFactor;

        } else if (i == 2) {
            text = "High Interest Rates\nThis year's second most damaging feature\nis its moderately high interest rates.";
            addInfo2 = avgInterestFactor;

        } else {
            text = "High Interest Rates\nThis year's third most damaging feature\nis its notably high interest rates.";
        }
    } else if (text == "Average Inflation Rate") {
        if (i == 1) {
            text = "High Inflation\nThis year's most damaging feature is its\nvery high rate of inflation.";
            addInfo1 = avgInflationFactor;

        } else if (i == 2) {
            text = "High Inflation\nThis year's second most damaging feature\nis its moderately high rate of inflation.";
            addInfo2 = avgInflationFactor;

        } else {
            text = "High Inflation\nThis year's third most damaging feature\nis its notably high rate of inflation.";
        }
    } else if (text == "Residential") {
        if (i == 1) {
            text = "Housing Availability\nThis year's most damaging feature is its\nremarkably low access to housing.";
            addInfo1 = residentialFactor;

        } else if (i == 2) {
            text = "Housing Availability\nThis year's second most damaging feature\nis its moderately low access to housing.";
            addInfo2 = residentialFactor;

        } else {
            text = "Housing Availability\nThis year's third most damaging feature\nis its notably low access to housing.";
        }
    } else if (text == "Average All Loans Default Rate") {
        if (i == 1) {
            text = "Default Rate - All Loans\nThis year's most damaging feature is its\nincredibly high default rate on all loans.";
            addInfo1 = allLoanDefaultFactor;

        } else if (i == 2) {
            text = "Default Rate - All Loans\nThis year's second most damaging feature\nis its moderately high default rate on all loans.";
            addInfo2 = allLoanDefaultFactor;

        } else {
            text = "Default Rate - All Loans\nThis year's third most damaging feature\nis its notably high default rate on all loans.";
        }
    } else if (text == "Consumer Confidence") {
        if (i == 1) {
            text = "Consumer Confidence\nThis year's most damaging feature is its\nvery low consumer confidence index.";
            addInfo1 = consumerConfidenceFactor;

        } else if (i == 2) {
            text = "Consumer Confidence\nThis year's second most damaging feature\nis its moderately low consumer confidence index.";
            addInfo2 = consumerConfidenceFactor;

        } else {
            text = "Consumer Confidence\nThis year's third most damaging feature\nis its notably low consumer confidence index.";
        }
    } else if (text == "Average Median Price") {
        if (i == 1) {
            text = "Housing Market\nThis year's most damaging feature is its\nseverely prohibitive housing market.";
            addInfo1 = medianPriceFactor;

        } else if (i == 2) {
            text = "Housing Market\nThis year's second most damaging feature is its\nmoderately prohibitive housing market.";
            addInfo2 = medianPriceFactor;

        } else {
            text = "Housing Market\nThis year's third most damaging feature is its\nnotably prohibitive housing market.";
        }
    } else if (text == "Year-In Change") {
        if (i == 1) {
            text = "Housing Price Change\nThis year's most damaging feature is its\nsevere change in housing prices.";
            addInfo1 = yearInChange;

        } else if (i == 2) {
            text = "Housing Price Change\nThis year's second most damaging feature\nis its moderate change in housing prices.";
            addInfo2 = yearInChange;

        } else {
            text = "Housing Price Change\nThis year's third most damaging feature\nis its notable change in housing prices.";
        }
    } else if (text == "Year-In Business Loan Default Change") {
        if (i == 1) {
            text = "Business Loan Defaults\nThis year experienced a massive increase in\nbusiness loan defaults.";
            addInfo1 = yearInBusinessLoanDefaultFactor;

        } else if (i == 2) {
            text = "Business Loan Defaults\nThis year experienced a moderate increase in\nbusiness loan defaults.";
            addInfo2 = yearInBusinessLoanDefaultFactor;

        } else {
            text = "Business Loan Defaults\nThis year experienced a notable increase in\nbusiness loan defaults.";
        }
    }
    return text;
}

void drawHighlight(HDC hdc, int top, int bottom, int left, int right, HBRUSH color, string text, int box) {
    if (box > 0)
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

void DrawDigitalClock(HDC hdc, int centerX, int centerY, int radius)
{
    // this will set up font and color for digital clock
    HFONT hFont = CreateFont(
            24,                // height of font
            0,                 // average character width
            0,                 // escapement angle
            0,                 // base-line orientation angle
            FW_BOLD,           // font weight
            FALSE,             // italic no
            FALSE,             // underline no
            FALSE,             // strikeout no
            ANSI_CHARSET,      // character set identifier
            OUT_TT_PRECIS,     // output precision
            CLIP_DEFAULT_PRECIS, // clipping precision
            ANTIALIASED_QUALITY, // output quality
            DEFAULT_PITCH,     // pitch and family
            "Arial");          // font

    HFONT hOldFont = (HFONT)SelectObject(hdc, hFont);
    COLORREF oldTextColor = SetTextColor(hdc, RGB(255, 0, 0));

    //draws dig clock
    std::stringstream ss;
    //time
    if (isDepression) {
        hour = hour;
        minute =  minute;
        second = second;
    }

    else {
        hour = 11 - hour;
        minute = 60 - minute;
        second = 60 - second;
    }


    string display_hour = to_string(hour);
    if (display_hour.length() < 2)
        display_hour = "0" + display_hour;
    string display_min = to_string(minute);
    if (display_min.length() < 2)
        display_min = "0" + display_min;
    string display_second = to_string(second);
    if (display_second.length() < 2)
        display_second = "0" + display_second;
    ss << display_hour << ":"  <<display_min << ":" << display_second;
    std::string timeStr = ss.str();

    RECT timeRect;
    SetRect(&timeRect, centerX - 50, centerY + radius + 10, centerX + 50, centerY + radius + 40);

    DrawText(hdc, timeStr.c_str(), -1, &timeRect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);

    // Cleanup
    SetTextColor(hdc, oldTextColor);
    SelectObject(hdc, hOldFont);
    DeleteObject(hFont);
}


// window procedure function
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    static HBRUSH black;
    static HBRUSH white;
    static HBRUSH grey;
    static HBRUSH red;
    static HBRUSH orange;
    static HBRUSH yellow;
    static HBRUSH blue;
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
            blue = CreateSolidBrush(RGB(174, 225, 255));

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
            int redY = -170;
            int orangeY = -70;
            int yellowY = 40;

            if (isDepression) {
                redY += 110;
                orangeY += 110;
                yellowY += 110;
            } else {
                redY = -170;
                orangeY = -70;
                yellowY = 40;
            }

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
                if (isDepression) {
                    drawHighlight(hdc, centerY - 170, centerY - 80, centerX + 120, centerX + 420, blue, disclaimerText, -1);
                }
                drawHighlight(hdc, centerY + redY, centerY + (redY + 90), centerX + 120, centerX + 420,
                              red, variables[highlights[currYear][0]], 1);
                drawHighlight(hdc, centerY + orangeY, centerY + (orangeY + 90), centerX + 120, centerX + 420,
                              orange, variables[highlights[currYear][1]], 2);
                drawHighlight(hdc, centerY + yellowY, centerY + (yellowY + 90), centerX + 120, centerX + 420,
                              yellow, variables[highlights[currYear][2]], 3);
                drawHighlight(hdc, centerY - 170, centerY +40, centerX-540, centerX - 120, grey, addInfo1, -1);
                drawHighlight(hdc, centerY +50, centerY+240, centerX-540, centerX - 120, grey, addInfo2, -1);

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
            DrawDigitalClock(hdc, centerX, centerY, radius);

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
