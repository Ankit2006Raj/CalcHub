/**
 * Data Visualization Charts
 * Using Chart.js for beautiful, animated charts
 */

// BMI Progress Chart
function createBMIProgressChart(containerId, bmiHistory) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: bmiHistory.map(item => item.date),
            datasets: [{
                label: 'BMI Progress',
                data: bmiHistory.map(item => item.bmi),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'BMI Progress Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function (value) {
                            return value.toFixed(1);
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Loan Amortization Chart
function createLoanAmortizationChart(containerId, principal, rate, duration) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;

    const months = duration * 12;
    const monthlyRate = rate / (12 * 100);
    const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) /
        (Math.pow(1 + monthlyRate, months) - 1);

    let balance = principal;
    const data = [];

    for (let month = 1; month <= Math.min(months, 60); month++) {
        const interestPayment = balance * monthlyRate;
        const principalPayment = emi - interestPayment;
        balance -= principalPayment;

        if (month % 6 === 0 || month === 1) {
            data.push({
                month: month,
                principal: principalPayment,
                interest: interestPayment,
                balance: Math.max(0, balance)
            });
        }
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => `Month ${d.month}`),
            datasets: [
                {
                    label: 'Principal Payment',
                    data: data.map(d => d.principal),
                    backgroundColor: '#2ecc71',
                    borderRadius: 5
                },
                {
                    label: 'Interest Payment',
                    data: data.map(d => d.interest),
                    backgroundColor: '#e74c3c',
                    borderRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Loan Amortization Schedule',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Attendance Improvement Chart
function createAttendanceChart(containerId, currentAttendance, targetAttendance, classesNeeded) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Present', 'Absent', 'Needed'],
            datasets: [{
                data: [currentAttendance, 100 - currentAttendance, classesNeeded],
                backgroundColor: [
                    '#2ecc71',
                    '#e74c3c',
                    '#f39c12'
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Attendance Overview',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000
            }
        }
    });
}

// GPA Distribution Chart
function createGPADistributionChart(containerId, courses) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;

    const gradePoints = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    };

    const colors = {
        'A+': '#2ecc71', 'A': '#2ecc71', 'A-': '#27ae60',
        'B+': '#3498db', 'B': '#3498db', 'B-': '#2980b9',
        'C+': '#f39c12', 'C': '#f39c12', 'C-': '#e67e22',
        'D+': '#e74c3c', 'D': '#e74c3c', 'F': '#c0392b'
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: courses.map(c => c.name || 'Course'),
            datasets: [{
                label: 'Grade Points',
                data: courses.map(c => gradePoints[c.grade] || 0),
                backgroundColor: courses.map(c => colors[c.grade] || '#95a5a6'),
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'GPA Distribution by Course',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const course = courses[context.dataIndex];
                            return [
                                'Grade: ' + course.grade,
                                'Points: ' + context.parsed.y.toFixed(2),
                                'Credits: ' + course.credits
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 4.0,
                    ticks: {
                        stepSize: 0.5
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Calorie Breakdown Chart
function createCalorieBreakdownChart(containerId, maintain, lose, gain) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Maintain Weight', 'Lose Weight', 'Gain Weight', 'Protein', 'Carbs', 'Fats'],
            datasets: [{
                label: 'Calorie Distribution',
                data: [maintain, lose, gain, maintain * 0.3, maintain * 0.4, maintain * 0.3],
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: '#667eea',
                borderWidth: 2,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Calorie & Macronutrient Distribution',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value + ' cal';
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Initialize charts when needed
function initializeCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded');
        return;
    }

    // Set global Chart.js defaults
    Chart.defaults.font.family = "'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif";
    Chart.defaults.color = '#333';
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCharts);
} else {
    initializeCharts();
}
