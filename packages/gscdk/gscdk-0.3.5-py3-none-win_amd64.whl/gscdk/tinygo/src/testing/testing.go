// Copyright 2009 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.
//
// This file has been modified for use by the TinyGo compiler.
// src: https://github.com/golang/go/blob/61bb56ad/src/testing/testing.go

// Package testing provides support for automated testing of Go packages.
package testing

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"strings"
)

// Testing flags.
var (
	flagVerbose bool
	flagShort   bool
)

var initRan bool

// Init registers testing flags. It has no effect if it has already run.
func Init() {
	if initRan {
		return
	}
	initRan = true

	flag.BoolVar(&flagVerbose, "test.v", false, "verbose: print additional output")
	flag.BoolVar(&flagShort, "test.short", false, "short: run smaller test suite to save time")
}

// common holds the elements common between T and B and
// captures common methods such as Errorf.
type common struct {
	output bytes.Buffer
	indent string

	failed   bool   // Test or benchmark has failed.
	skipped  bool   // Test of benchmark has been skipped.
	finished bool   // Test function has completed.
	name     string // Name of test or benchmark.
}

// TB is the interface common to T and B.
type TB interface {
	Error(args ...interface{})
	Errorf(format string, args ...interface{})
	Fail()
	FailNow()
	Failed() bool
	Fatal(args ...interface{})
	Fatalf(format string, args ...interface{})
	Log(args ...interface{})
	Logf(format string, args ...interface{})
	Name() string
	Skip(args ...interface{})
	SkipNow()
	Skipf(format string, args ...interface{})
	Skipped() bool
	Helper()
	Parallel()
}

var _ TB = (*T)(nil)
var _ TB = (*B)(nil)

// T is a type passed to Test functions to manage test state and support formatted test logs.
// Logs are accumulated during execution and dumped to standard output when done.
//
type T struct {
	common
}

// Name returns the name of the running test or benchmark.
func (c *common) Name() string {
	return c.name
}

// Fail marks the function as having failed but continues execution.
func (c *common) Fail() {
	c.failed = true
}

// Failed reports whether the function has failed.
func (c *common) Failed() bool {
	failed := c.failed
	return failed
}

// FailNow marks the function as having failed and stops its execution
// by calling runtime.Goexit (which then runs all deferred calls in the
// current goroutine).
func (c *common) FailNow() {
	c.Fail()

	c.finished = true
	c.Error("FailNow is incomplete, requires runtime.Goexit()")
}

// log generates the output.
func (c *common) log(s string) {
	// This doesn't print the same as in upstream go, but works for now.
	if len(s) != 0 && s[len(s)-1] == '\n' {
		s = s[:len(s)-1]
	}
	lines := strings.Split(s, "\n")
	// First line.
	c.output.WriteString(c.indent)
	c.output.WriteString("    ") // 4 spaces
	c.output.WriteString(lines[0])
	c.output.WriteByte('\n')
	// More lines.
	for _, line := range lines[1:] {
		c.output.WriteString(c.indent)
		c.output.WriteString("        ") // 8 spaces
		c.output.WriteString(line)
		c.output.WriteByte('\n')
	}
}

// Log formats its arguments using default formatting, analogous to Println,
// and records the text in the error log. For tests, the text will be printed only if
// the test fails or the -test.v flag is set. For benchmarks, the text is always
// printed to avoid having performance depend on the value of the -test.v flag.
func (c *common) Log(args ...interface{}) { c.log(fmt.Sprintln(args...)) }

// Logf formats its arguments according to the format, analogous to Printf, and
// records the text in the error log. A final newline is added if not provided. For
// tests, the text will be printed only if the test fails or the -test.v flag is
// set. For benchmarks, the text is always printed to avoid having performance
// depend on the value of the -test.v flag.
func (c *common) Logf(format string, args ...interface{}) { c.log(fmt.Sprintf(format, args...)) }

// Error is equivalent to Log followed by Fail.
func (c *common) Error(args ...interface{}) {
	c.log(fmt.Sprintln(args...))
	c.Fail()
}

// Errorf is equivalent to Logf followed by Fail.
func (c *common) Errorf(format string, args ...interface{}) {
	c.log(fmt.Sprintf(format, args...))
	c.Fail()
}

// Fatal is equivalent to Log followed by FailNow.
func (c *common) Fatal(args ...interface{}) {
	c.log(fmt.Sprintln(args...))
	c.FailNow()
}

// Fatalf is equivalent to Logf followed by FailNow.
func (c *common) Fatalf(format string, args ...interface{}) {
	c.log(fmt.Sprintf(format, args...))
	c.FailNow()
}

// Skip is equivalent to Log followed by SkipNow.
func (c *common) Skip(args ...interface{}) {
	c.log(fmt.Sprintln(args...))
	c.SkipNow()
}

// Skipf is equivalent to Logf followed by SkipNow.
func (c *common) Skipf(format string, args ...interface{}) {
	c.log(fmt.Sprintf(format, args...))
	c.SkipNow()
}

// SkipNow marks the test as having been skipped and stops its execution
// by calling runtime.Goexit.
func (c *common) SkipNow() {
	c.skip()
	c.finished = true
	c.Error("SkipNow is incomplete, requires runtime.Goexit()")
}

func (c *common) skip() {
	c.skipped = true
}

// Skipped reports whether the test was skipped.
func (c *common) Skipped() bool {
	return c.skipped
}

// Helper is not implemented, it is only provided for compatibility.
func (c *common) Helper() {
	// Unimplemented.
}

// Parallel is not implemented, it is only provided for compatibility.
func (c *common) Parallel() {
	// Unimplemented.
}

// Run runs a subtest of f t called name. It waits until the subtest is finished
// and returns whether the subtest succeeded.
func (t *T) Run(name string, f func(t *T)) bool {
	// Create a subtest.
	sub := T{
		common: common{
			name:   t.name + "/" + name,
			indent: t.indent + "    ",
		},
	}

	// Run the test.
	if flagVerbose {
		fmt.Fprintf(&t.output, "=== RUN   %s\n", sub.name)

	}
	f(&sub)

	// Process the result (pass or fail).
	if sub.failed {
		t.failed = true
		fmt.Fprintf(&t.output, sub.indent+"--- FAIL: %s\n", sub.name)
		t.output.Write(sub.output.Bytes())
	} else {
		if flagVerbose {
			fmt.Fprintf(&t.output, sub.indent+"--- PASS: %s\n", sub.name)
			t.output.Write(sub.output.Bytes())
		}
	}
	return !sub.failed
}

// InternalTest is a reference to a test that should be called during a test suite run.
type InternalTest struct {
	Name string
	F    func(*T)
}

// M is a test suite.
type M struct {
	// tests is a list of the test names to execute
	Tests []InternalTest
}

// Run the test suite.
func (m *M) Run() int {
	if len(m.Tests) == 0 {
		fmt.Fprintln(os.Stderr, "testing: warning: no tests to run")
	}

	if !flag.Parsed() {
		flag.Parse()
	}

	failures := 0
	for _, test := range m.Tests {
		t := &T{
			common: common{
				name: test.Name,
			},
		}

		if flagVerbose {
			fmt.Printf("=== RUN   %s\n", test.Name)
		}
		test.F(t)

		if t.failed {
			fmt.Printf("--- FAIL: %s\n", test.Name)
			os.Stdout.Write(t.output.Bytes())
		} else {
			if flagVerbose {
				fmt.Printf("--- PASS: %s\n", test.Name)
				os.Stdout.Write(t.output.Bytes())
			}
		}

		if t.failed {
			failures++
		}
	}

	if failures > 0 {
		fmt.Println("FAIL")
	} else {
		if flagVerbose {
			fmt.Println("PASS")
		}
	}
	return failures
}

// Short reports whether the -test.short flag is set.
func Short() bool {
	return flagShort
}

// Verbose reports whether the -test.v flag is set.
func Verbose() bool {
	return flagVerbose
}

// AllocsPerRun returns the average number of allocations during calls to f.
// Although the return value has type float64, it will always be an integral
// value.
//
// Not implemented.
func AllocsPerRun(runs int, f func()) (avg float64) {
	f()
	for i := 0; i < runs; i++ {
		f()
	}
	return 0
}

func TestMain(m *M) {
	os.Exit(m.Run())
}

func MainStart(deps interface{}, tests []InternalTest, benchmarks []InternalBenchmark, examples []InternalExample) *M {
	Init()
	return &M{
		Tests: tests,
	}
}

type InternalExample struct {
	Name      string
	F         func()
	Output    string
	Unordered bool
}
